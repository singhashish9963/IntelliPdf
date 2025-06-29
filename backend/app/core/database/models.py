from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship, declarative_base
from pgvector.sqlalchemy import Vector
import datetime

Base = declarative_base()

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    file_path = Column(String, nullable=True)
    minio_key = Column(String(255), nullable=True)       # MinIO object key
    neo4j_node_id = Column(String(128), nullable=True)   # Neo4j node id or UUID
    doc_metadata = Column(JSON, nullable=True)
    embedding = Column(Vector(384), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    chunks = relationship("Chunk", back_populates="document")

class Chunk(Base):
    __tablename__ = "chunks"
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), index=True)
    text = Column(String)
    page_number = Column(Integer, nullable=True)
    chunk_type = Column(String, nullable=True)
    embedding = Column(Vector(384), nullable=True)
    doc_metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    document = relationship("Document", back_populates="chunks")