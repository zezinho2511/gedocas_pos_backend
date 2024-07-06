from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from models import Session, Smallword
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
smallword_tag = Tag(name="Smallword", description="Adição, visualização e remoção de minimundo à base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/api/minimundo', tags=[smallword_tag],
          responses={"200": SmallwordViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_smallword(form: SmallwordSchema):
    """Adiciona um novo Minimundo à base de dados

    Retorna uma representação dos minimundos associados.
    """
    smallword = Smallword(
        name=form.name,
        type=form.type,
        description=form.description
    )
    logger.info(f"Adicionando cliente desse minimundo: '{smallword.name}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando minimundo
        session.add(smallword)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.info("Adicionado minimundo: %s" % smallword)
        return apresenta_smallword(smallword), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Minimundo de mesmo nome e marca já salvo na base :/"
        logger.warning(f"Erro ao adicionar o cliente e seu minimundo '{smallword.name}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar o cliente e seu minimundo '{smallword.name}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/api/minimundos', tags=[smallword_tag],
         responses={"200": ListagemSmallwordsSchema, "404": ErrorSchema})
def get_smallwords():
    """Faz a busca por todos os Minimundo cadastrados

    Retorna uma representação da listagem de minimundos.
    """
    logger.info(f"Coletando minimundos ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    smallwords = session.query(Smallword).all()

    if not smallwords:
        # se não há minimundos cadastrados
        return {"minimundos": []}, 200
    else:
        logger.info(f"%d minimundos econtrados" % len(smallwords))
        # retorna a representação de minimundo
        return apresenta_smallwords(smallwords), 200


@app.get('/api/minimundo', tags=[smallword_tag],
         responses={"200": SmallwordViewSchema, "404": ErrorSchema})
def get_smallword(query: SmallwordBuscaPorIDSchema):
    """Faz a busca por um Minimundo a partir do id do minimundo

    Retorna uma representação dos minimundos e comentários associados.
    """
    smallword_id = query.id
    logger.info(f"Coletando dados sobre minimundo #{smallword_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    smallword = session.query(Smallword).filter(Smallword.id == smallword_id).first()

    if not smallword:
        # se o minimundo não foi encontrado
        error_msg = "Minimundo não encontrado na base :/"
        logger.warning(f"Erro ao buscar minimundo '{smallword_id}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.info("Minimundo econtrado: %s" % smallword)
        # retorna a representação de minimundo
        return apresenta_smallword(smallword), 200


@app.delete('/api/minimundo', tags=[smallword_tag],
            responses={"200": SmallwordDelSchema, "404": ErrorSchema})
def del_smallword(query: SmallwordBuscaPorIDSchema):
    """Deleta um Minimundo a partir do id informado

    Retorna uma mensagem de confirmação da remoção.
    """
    logger.info(f"Deletando dados sobre minimundo #{query.id}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Smallword).filter(Smallword.id == query.id).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.info(f"Deletado minimundo #{query.id}")
        return {"mesage": "Minimundo removido", "id": query.id}
    else:
        # se o minimundo não foi encontrado
        error_msg = "Minimundo não encontrado na base :/"
        logger.warning(f"Erro ao deletar minimundo #'{query.id}', {error_msg}")
        return {"mesage": error_msg}, 404


@app.get('/api/busca_minimundo', tags=[smallword_tag],
         responses={"200": ListagemSmallwordsSchema, "404": ErrorSchema})
def busca_smallword(query: SmallwordBuscaPorNomeSchema):
    """Faz a busca por minimundos em que o termo passando  Minimundo a partir do id do minimundo

    Retorna uma representação dos minimundos e comentários associados.
    """
    termo = unquote(query.termo)
    logger.info(f"Fazendo a busca por nome com o termo: {termo}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    smallwords = session.query(Smallword).filter(Smallword.name.ilike(f"%{termo}%")).all()

    if not smallwords:
        # se não há minimundos cadastrados
        return {"minimundos": []}, 200
    else:
        logger.info(f"%d rodutos econtrados" % len(smallwords))
        # retorna a representação de minimundo
        return apresenta_smallwords(smallwords)