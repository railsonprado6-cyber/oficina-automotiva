from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from app.config import Base

# ==================== USUÁRIOS ====================
class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    senha_hash = Column(String(255))
    nome_completo = Column(String(150))
    ativo = Column(Boolean, default=True)
    perfil = Column(String(20))  # admin, atendente, tecnico, estoque
    data_criacao = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    ordens_servico = relationship("OrdenServico", back_populates="tecnico")


# ==================== CLIENTES ====================
class Cliente(Base):
    __tablename__ = "clientes"
    
    id = Column(Integer, primary_key=True, index=True)
    nome_completo = Column(String(150), index=True)
    telefone = Column(String(20))
    whatsapp = Column(String(20))
    cpf = Column(String(14), unique=True, index=True, nullable=True)
    cnpj = Column(String(18), unique=True, index=True, nullable=True)
    endereco = Column(String(255))
    bairro = Column(String(100))
    cidade = Column(String(100))
    estado = Column(String(2))
    cep = Column(String(9))
    observacoes = Column(Text, nullable=True)
    ativo = Column(Boolean, default=True)
    data_criacao = Column(DateTime, default=datetime.utcnow)
    data_atualizacao = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    veiculos = relationship("Veiculo", back_populates="cliente", cascade="all, delete-orphan")
    ordens_servico = relationship("OrdenServico", back_populates="cliente")


# ==================== VEÍCULOS ====================
class Veiculo(Base):
    __tablename__ = "veiculos"
    
    id = Column(Integer, primary_key=True, index=True)
    placa = Column(String(10), unique=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), index=True)
    marca = Column(String(50))
    modelo = Column(String(100))
    ano = Column(Integer)
    cor = Column(String(50), nullable=True)
    quilometragem_atual = Column(Integer, default=0)
    numero_motor = Column(String(50), nullable=True)
    numero_chassis = Column(String(50), nullable=True)
    observacoes = Column(Text, nullable=True)
    ativo = Column(Boolean, default=True)
    data_criacao = Column(DateTime, default=datetime.utcnow)
    data_atualizacao = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    cliente = relationship("Cliente", back_populates="veiculos")
    ordens_servico = relationship("OrdenServico", back_populates="veiculo", cascade="all, delete-orphan")
    historico_servicos = relationship("HistoricoServico", back_populates="veiculo", cascade="all, delete-orphan")


# ==================== ORDENS DE SERVIÇO ====================
class OrdenServico(Base):
    __tablename__ = "ordens_servico"
    
    id = Column(Integer, primary_key=True, index=True)
    numero_os = Column(String(20), unique=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), index=True)
    veiculo_id = Column(Integer, ForeignKey("veiculos.id"), index=True)
    tecnico_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    quilometragem_entrada = Column(Integer)
    quilometragem_saida = Column(Integer, nullable=True)
    data_abertura = Column(DateTime, default=datetime.utcnow, index=True)
    data_conclusao = Column(DateTime, nullable=True)
    status = Column(String(20), default="aberta")  # aberta, em_andamento, concluida, cancelada
    forma_pagamento = Column(String(50), nullable=True)
    valor_mao_obra = Column(Float, default=0)
    valor_pecas = Column(Float, default=0)
    valor_total = Column(Float, default=0)
    desconto = Column(Float, default=0)
    observacoes = Column(Text, nullable=True)
    assinatura_cliente = Column(Text, nullable=True)  # Base64 ou caminho
    
    # Relacionamentos
    cliente = relationship("Cliente", back_populates="ordens_servico")
    veiculo = relationship("Veiculo", back_populates="ordens_servico")
    tecnico = relationship("Usuario", back_populates="ordens_servico")
    servicos = relationship("Servico", back_populates="ordem_servico", cascade="all, delete-orphan")
    pecas_utilizadas = relationship("PecaOrdenServico", back_populates="ordem_servico", cascade="all, delete-orphan")


# ==================== SERVIÇOS ====================
class Servico(Base):
    __tablename__ = "servicos"
    
    id = Column(Integer, primary_key=True, index=True)
    ordem_servico_id = Column(Integer, ForeignKey("ordens_servico.id"), index=True)
    descricao = Column(String(255))
    valor = Column(Float)
    tempo_estimado = Column(Integer, nullable=True)  # em minutos
    observacoes = Column(Text, nullable=True)
    data_criacao = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    ordem_servico = relationship("OrdenServico", back_populates="servicos")


# ==================== HISTÓRICO DE SERVIÇOS ====================
class HistoricoServico(Base):
    __tablename__ = "historico_servicos"
    
    id = Column(Integer, primary_key=True, index=True)
    veiculo_id = Column(Integer, ForeignKey("veiculos.id"), index=True)
    ordem_servico_id = Column(Integer, ForeignKey("ordens_servico.id"), nullable=True)
    descricao = Column(String(255))
    data_servico = Column(DateTime, index=True)
    quilometragem = Column(Integer)
    tecnico_responsavel = Column(String(150))
    valor_mao_obra = Column(Float)
    valor_pecas = Column(Float, default=0)
    valor_total = Column(Float)
    observacoes = Column(Text, nullable=True)
    
    # Relacionamentos
    veiculo = relationship("Veiculo", back_populates="historico_servicos")


# ==================== PEÇAS ====================
class Peca(Base):
    __tablename__ = "pecas"
    
    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(50), unique=True, index=True)
    nome = Column(String(200), index=True)
    descricao = Column(Text, nullable=True)
    marca = Column(String(100))
    preco_custo = Column(Float)
    preco_venda = Column(Float)
    quantidade_disponivel = Column(Integer, default=0)
    quantidade_minima = Column(Integer, default=5)
    fornecedor_id = Column(Integer, ForeignKey("fornecedores.id"), nullable=True)
    ativo = Column(Boolean, default=True)
    data_criacao = Column(DateTime, default=datetime.utcnow)
    data_atualizacao = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    fornecedor = relationship("Fornecedor", back_populates="pecas")
    movimentacoes = relationship("MovimentacaoEstoque", back_populates="peca", cascade="all, delete-orphan")


# ==================== PEÇAS UTILIZADAS EM OS ====================
class PecaOrdenServico(Base):
    __tablename__ = "pecas_ordem_servico"
    
    id = Column(Integer, primary_key=True, index=True)
    ordem_servico_id = Column(Integer, ForeignKey("ordens_servico.id"), index=True)
    peca_id = Column(Integer, ForeignKey("pecas.id"), index=True)
    quantidade = Column(Integer, default=1)
    preco_unitario = Column(Float)
    valor_total = Column(Float)
    
    # Relacionamentos
    ordem_servico = relationship("OrdenServico", back_populates="pecas_utilizadas")
    peca = relationship("Peca")


# ==================== FORNECEDORES ====================
class Fornecedor(Base):
    __tablename__ = "fornecedores"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150), unique=True, index=True)
    telefone = Column(String(20))
    email = Column(String(100))
    endereco = Column(String(255))
    cnpj = Column(String(18), nullable=True)
    contato = Column(String(150))
    ativo = Column(Boolean, default=True)
    data_criacao = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    pecas = relationship("Peca", back_populates="fornecedor")


# ==================== MOVIMENTAÇÃO DE ESTOQUE ====================
class MovimentacaoEstoque(Base):
    __tablename__ = "movimentacoes_estoque"
    
    id = Column(Integer, primary_key=True, index=True)
    peca_id = Column(Integer, ForeignKey("pecas.id"), index=True)
    tipo = Column(String(20))  # entrada, saida
    quantidade = Column(Integer)
    preco_unitario = Column(Float, nullable=True)
    valor_total = Column(Float, nullable=True)
    motivo = Column(String(255), nullable=True)
    ordem_servico_id = Column(Integer, ForeignKey("ordens_servico.id"), nullable=True)
    data_movimentacao = Column(DateTime, default=datetime.utcnow, index=True)
    usuario_responsavel = Column(String(150))
    observacoes = Column(Text, nullable=True)
    
    # Relacionamentos
    peca = relationship("Peca", back_populates="movimentacoes")
