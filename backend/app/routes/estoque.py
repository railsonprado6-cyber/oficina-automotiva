from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config import get_db
from app.schemas import Peca, PecaCreate, PecaUpdate, MovimentacaoEstoque, MovimentacaoEstoqueCreate
from app.models import Peca as PecaModel, MovimentacaoEstoque as MovimentacaoModel
from app.services.business_service import EstoqueService

router = APIRouter(prefix="/estoque", tags=["estoque"])

@router.post("/pecas/", response_model=Peca)
def criar_peca(peca: PecaCreate, db: Session = Depends(get_db)):
    """Cadastrar nova peça"""
    db_peca = PecaModel(**peca.dict())
    db.add(db_peca)
    db.commit()
    db.refresh(db_peca)
    return db_peca

@router.get("/pecas/", response_model=list[Peca])
def listar_pecas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Listar todas as peças"""
    return db.query(PecaModel).filter(PecaModel.ativo == True).offset(skip).limit(limit).all()

@router.get("/pecas/{peca_id}", response_model=Peca)
def obter_peca(peca_id: int, db: Session = Depends(get_db)):
    """Obter peça por ID"""
    db_peca = db.query(PecaModel).filter(PecaModel.id == peca_id).first()
    if not db_peca:
        raise HTTPException(status_code=404, detail="Peça não encontrada")
    return db_peca

@router.get("/pecas/codigo/{codigo}", response_model=Peca)
def obter_peca_codigo(codigo: str, db: Session = Depends(get_db)):
    """Obter peça por código"""
    db_peca = db.query(PecaModel).filter(PecaModel.codigo == codigo).first()
    if not db_peca:
        raise HTTPException(status_code=404, detail="Peça não encontrada")
    return db_peca

@router.put("/pecas/{peca_id}", response_model=Peca)
def atualizar_peca(peca_id: int, peca: PecaUpdate, db: Session = Depends(get_db)):
    """Atualizar peça"""
    db_peca = db.query(PecaModel).filter(PecaModel.id == peca_id).first()
    if not db_peca:
        raise HTTPException(status_code=404, detail="Peça não encontrada")
    
    update_data = peca.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_peca, field, value)
    
    db.commit()
    db.refresh(db_peca)
    return db_peca

@router.get("/alerta/estoque-baixo/")
def alertas_estoque_baixo(db: Session = Depends(get_db)):
    """Listar peças com estoque baixo"""
    pecas_baixas = EstoqueService.get_pecas_estoque_baixo(db)
    return {
        "total_alertas": len(pecas_baixas),
        "pecas": [
            {
                "id": p.id,
                "codigo": p.codigo,
                "nome": p.nome,
                "quantidade_disponivel": p.quantidade_disponivel,
                "quantidade_minima": p.quantidade_minima
            }
            for p in pecas_baixas
        ]
    }

@router.post("/movimentacoes/", response_model=MovimentacaoEstoque)
def registrar_movimentacao(mov: MovimentacaoEstoqueCreate, db: Session = Depends(get_db)):
    """Registrar entrada/saída de peça"""
    resultado = EstoqueService.registrar_movimentacao(
        db,
        peca_id=mov.peca_id,
        tipo=mov.tipo,
        quantidade=mov.quantidade,
        usuario_responsavel="usuario",  # TODO: usar usuário autenticado
        preco_unitario=mov.preco_unitario,
        motivo=mov.motivo,
        ordem_servico_id=mov.ordem_servico_id
    )
    return resultado

@router.get("/movimentacoes/", response_model=list[MovimentacaoEstoque])
def listar_movimentacoes(peca_id: int = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Listar movimentações de estoque"""
    query = db.query(MovimentacaoModel)
    if peca_id:
        query = query.filter(MovimentacaoModel.peca_id == peca_id)
    return query.order_by(MovimentacaoModel.data_movimentacao.desc()).offset(skip).limit(limit).all()

@router.get("/movimentacoes/{peca_id}/historico", response_model=list[MovimentacaoEstoque])
def historico_peca(peca_id: int, db: Session = Depends(get_db)):
    """Histórico completo de movimentações de uma peça"""
    return db.query(MovimentacaoModel).filter(
        MovimentacaoModel.peca_id == peca_id
    ).order_by(MovimentacaoModel.data_movimentacao.desc()).all()
