# -*- encoding:utf-8 -*-
"""
    数据库表
"""
from sqlalchemy import ForeignKey
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer,String, DECIMAL,TIMESTAMP,Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()
class Datadetails(Base):
    __tablename__ = 'datadetails'
    DataDetailsId = Column(String(50), primary_key=True)
    DataPacketId = Column(String(50))
    Interval = Column(String(10))
    TradeType = Column(String(10))
    Exchange = Column(String(50))
    Type = Column(String(10))
    Symbol = Column(String(255))
    DataType = Column(String(10))
    Start = Column(DateTime)
    End = Column(DateTime)


class Datapacket(Base):
    __tablename__ = 'datapacket'
    DatapacketId = Column(String(50), primary_key=True)
    Name = Column(String(200))
    Msg = Column(String(255))
    Grade = Column(String(20))
    Exchange = Column(String(50))
    Type = Column(String(255))

class Backtest(Base):
    __tablename__ = 'backtest'
    Id = Column(String(50), primary_key=True)
    StrategyId = Column(String(50))
    Amount = Column(DECIMAL(50))
    Status = Column(String(10))
    BacktestTime = Column(TIMESTAMP)
    StartTime = Column(TIMESTAMP)
    EndTime = Column(TIMESTAMP)
    CumPnlRatio = Column(DECIMAL(6))
    MaxDrawdown = Column(DECIMAL(6))
    SharpRatio = Column(DECIMAL(6))
    Remark = Column(String(50))
    CreatedAt = Column(TIMESTAMP)
    UpdatedAt = Column(TIMESTAMP)

class Backtestresult(Base):
    __tablename__ = 'backtestresult'
    BacktestId = Column(String(255), primary_key=True)
    BacktestReuslt = Column(Text)
    CreatedAt = Column(DateTime)

class BacktestInfo(Base):
    __tablename__ = 'backtestinfo'
    BacktestId = Column(String(255), primary_key=True)
    BacktestParam = Column(Text)
    CreatedAt = Column(DateTime)
    UpdatedAt = Column(DateTime)   

class Logs(Base):
    __tablename__ = 'logs'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    BacktestId = Column(String(50))
    Log = Column(Text)
    Level = Column(String(10))
    CreatedAt = Column(TIMESTAMP)
    UpdatedAt = Column(TIMESTAMP)

class Strategy(Base):
    __tablename__ = 'strategy'
    Id = Column(String(50), primary_key=True)
    UserId = Column(String(50))
    Name = Column(String(50))
    BacktestNum = Column(Integer)
    Remark = Column(Text)
    CreatedAt = Column(TIMESTAMP)
    UpdatedAt = Column(TIMESTAMP)

class Strategyorder(Base):
    __tablename__ = 'strategyorder'
    Id = Column(Integer, primary_key=True,autoincrement=True)
    Symbol = Column(String(255))
    Direction = Column(String(255))
    Offset = Column(String(255))
    OrderType = Column(Integer)
    LimitPrice = Column(DECIMAL(2))
    FillPrice = Column(DECIMAL(2))
    VolumeMultiple = Column(String(255))
    Quantity = Column(DECIMAL(4))
    StrategyId = Column(String(100))
    OrderTime = Column(DateTime)
    JobId = Column(String(100))
    OrderFee = Column(String(255))
    Status = Column(String(255))
    FillTime = Column(DateTime)
    OrderResult = Column(String(255))
    OrderId = Column(String(255))
    OperateTime = Column(DateTime)
    CloseProfit = Column(DECIMAL(4))
    CreatedAt = Column(DateTime)
    UpdatedAt = Column(DateTime)
    Nav = Column(DECIMAL(4))
    Cach = Column(DECIMAL(4))
    CloseProfitRatio = Column(DECIMAL(4))
    PositionId = Column(String(255))

class Position(Base):
    __tablename__ = 'position'
    Id = Column(Integer, primary_key=True,autoincrement=True)
    PositionId = Column(String(255))
    BacktestId = Column(String(255))
    Symbol = Column(String(255))
    Direction = Column(String(255))
    CreatedAt = Column(DateTime)

class PaperPosition(Base):
    __tablename__ = 'paperposition'
    Id = Column(Integer, primary_key=True,autoincrement=True)
    PositionId = Column(String(255))
    PaperId = Column(String(255))
    Symbol = Column(String(255))
    Direction = Column(String(255))
    CreatedAt = Column(DateTime)