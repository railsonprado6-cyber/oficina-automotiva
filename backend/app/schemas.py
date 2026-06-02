from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr

# ==================== USUARIO ====================
class UsuarioBase(BaseModel):
    username: str
    email: EmailStr
    nome_completo: str
    perfil: str

class UsuarioCreate(UsuarioBase):
    senha: str

class UsuarioUpdate(BaseModel):
    email: Optional[EmailStr] = None
    nome_completo: Optional[str] = None
    ativo: Optional[bool] = None

class Usuario(UsuarioBase):
    id: int
    ativo: bool
    data_criacao: datetime
    
    class Config:
        from_attributes = True

# ==================== CLIENTE ====================
class ClienteBase(BaseModel):
    nome_completo: str
    telefone: str
    whatsapp: Optional[str] = None
    cpf: Optional[str] = None
    cnpj: Optional[str] = None
    endereco: str
    bairro: str
    cidade: str
    estado: str
    cep: str
    observacoes: Optional[str] = None

class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(BaseModel):
    nome_completo: Optional[str] = None
    telefone: Optional[str] = None
    whatsapp: Optional[str] = None
    endereco: Optional[str] = None
    observacoes: Optional[str] = None
    ativo: Optional[bool] = None

class Cliente(ClienteBase):
    id: int
    ativo: bool
    data_criacao: datetime
    data_atualizacao: datetime
    
    class Config:
        from_attributes = True

# ==================== VEICULO ====================
class VeiculoBase(BaseModel):
    placa: str
    cliente_id: int
    marca: str
    modelo: str
    ano: int
    cor: Optional[str] = None
    quilometragem_atual: int
    numero_motor: Optional[str] = None
    numero_chassis: Optional[str] = None
    observacoes: Optional[str] = None

class VeiculoCreate(VeiculoBase):
    pass

class VeiculoUpdate(BaseModel):
    quilometragem_atual: Optional[int] = None
    observacoes: Optional[str] = None
    ativo: Optional[bool] = None

class Veiculo(VeiculoBase):
    id: int
    ativo: bool
    data_criacao: datetime
    data_atualizacao: datetime
    
    class Config:
        from_attributes = True

# ==================== ORDEM DE SERVIÇO ====================
class ServicoCreate(BaseModel):
    descricao: str
    valor: float
    tempo_estimado: Optional[int] = None
    observacoes: Optional[str] = None

class Servico(ServicoCreate):
    id: int
    ordem_servico_id: int
    data_criacao: datetime
    
    class Config:
        from_attributes = True

class PecaOrdenServicoCreate(BaseModel):
    peca_id: int
    quantidade: int
    preco_unitario: float

class PecaOrdenServico(PecaOrdenServicoCreate):
    id: int
    valor_total: float
    
    class Config:
        from_attributes = True

class OrdenServicoBase(BaseModel):
    cliente_id: int
    veiculo_id: int
    quilometragem_entrada: int
    tecnico_id: Optional[int] = None
    forma_pagamento: Optional[str] = None
    observacoes: Optional[str] = None

class OrdenServicoCreate(OrdenServicoBase):
    pass

class OrdenServicoUpdate(BaseModel):
    status: Optional[str] = None
    quilometragem_saida: Optional[int] = None
    tecnico_id: Optional[int] = None
    forma_pagamento: Optional[str] = None
    observacoes: Optional[str] = None
    assinatura_cliente: Optional[str] = None

class OrdenServico(OrdenServicoBase):
    id: int
    numero_os: str
    status: str
    valor_mao_obra: float
    valor_pecas: float
    valor_total: float
    desconto: float
    quilometragem_saida: Optional[int]
    data_abertura: datetime
    data_conclusao: Optional[datetime]
    servicos: List[Servico] = []
    pecas_utilizadas: List[PecaOrdenServico] = []
    
    class Config:
        from_attributes = True

# ==================== PEÇA ====================
class PecaBase(BaseModel):
    codigo: str
    nome: str
    descricao: Optional[str] = None
    marca: str
    preco_custo: float
    preco_venda: float
    quantidade_disponivel: int
    quantidade_minima: int
    fornecedor_id: Optional[int] = None

class PecaCreate(PecaBase):
    pass

class PecaUpdate(BaseModel):
    nome: Optional[str] = None
    preco_venda: Optional[float] = None
    quantidade_disponivel: Optional[int] = None
    ativo: Optional[bool] = None

class Peca(PecaBase):
    id: int
    ativo: bool
    data_criacao: datetime
    data_atualizacao: datetime
    
    class Config:
        from_attributes = True

# ==================== FORNECEDOR ====================
class FornecedorBase(BaseModel):
    nome: str
    telefone: str
    email: str
    endereco: str
    contato: str
    cnpj: Optional[str] = None

class FornecedorCreate(FornecedorBase):
    pass

class Fornecedor(FornecedorBase):
    id: int
    ativo: bool
    data_criacao: datetime
    
    class Config:
        from_attributes = True

# ==================== MOVIMENTAÇÃO ESTOQUE ====================
class MovimentacaoEstoqueCreate(BaseModel):
    peca_id: int
    tipo: str  # entrada, saida
    quantidade: int
    preco_unitario: Optional[float] = None
    motivo: Optional[str] = None
    ordem_servico_id: Optional[int] = None
    observacoes: Optional[str] = None

class MovimentacaoEstoque(MovimentacaoEstoqueCreate):
    id: int
    valor_total: Optional[float]
    data_movimentacao: datetime
    usuario_responsavel: str
    
    class Config:
        from_attributes = True

# ==================== RESPOSTA BUSCA PLACA ====================
class BuscaPlacaResponse(BaseModel):
    cliente: Cliente
    veiculo: Veiculo
    ordens_servico: List[OrdenServico] = []
    historico_servicos: List[dict] = []
    
    class Config:
        from_attributes = True
