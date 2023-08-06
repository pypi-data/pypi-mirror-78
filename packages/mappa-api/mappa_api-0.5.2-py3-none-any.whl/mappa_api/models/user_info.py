from datetime import datetime

from pydantic import BaseModel


class UserInfo(BaseModel):
    id: int     # escotista.codigo
    username: str  # escotista.username
    codigoAssociado: int    # Número na carteira UEB (Escotista)
    numeroDigito: int       # Dígito na carteira UEB (Associado)
    nomeCompleto: str        # Escotista
    nomeAbreviado: str       # Associado
    dataNascimento: datetime  # A
    sexo: str                # A
    ativo: bool              # escotista.ativo=='S'
    dataValidade: datetime   # A
    codigoGrupo: int         # E
    codigoRegiao: str        # E
    nomeGrupo: str           # grupo.nome
    codigoModalidade: int   # grupo.codigoModalidade
    autorizacao: str         # login
    autorizacaoValidade: int  # login (timestamp)
