# -*- encoding: utf-8 -*-
'''
@文件    :tables.py
@说明    :
@时间    :2020/09/02 11:46:41
@作者    :caimmy@hotmail.com
@版本    :0.1
'''

from datetime import datetime, date

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Enum, DateTime, TEXT, JSON, ForeignKey
from sqlalchemy.orm import relationship, backref

Base = declarative_base()

def model_property_to_dict(self, hashid_properties=[]):
    """
    对模型的属性遍历并转换到字典
    :param self:
    :param hashid_properties: 针对列表的属性，需要做hashids
    :return:
    """
    ret_dict = {}
    for c in self.__table__.columns:
        if c.name in ('create_ip', 'status', 'creater'):
            continue
        elif isinstance(getattr(self, c.name, ""), (datetime, date)):
            ret_dict.setdefault(c.name, str(getattr(self, c.name, "")))
        else:
            ret_dict.setdefault(c.name, getattr(self, c.name, ""))
    return ret_dict

if not hasattr(Base, "property2Dict"):
    Base.property2Dict = model_property_to_dict

class TblFlowRule(Base):
    __tablename__ = "karuo_flow"

    id              = Column(Integer, primary_key=True, autoincrement=True)
    prev_id         = Column(Integer, nullable=False, comment="前序节点规则编号")
    icon            = Column(String(512), default="", comment="流程的ICON")
    publisher       = Column(String(128), default="", comment="发布者")
    catalog         = Column(String(128), nullable=False, comment="审批类型")
    name            = Column(String(128), nullable=False, comment="审批名称")
    node_label      = Column(String(64), nullable=False, comment="节点标识")
    reviewer        = Column(JSON, comment="决策者列表 json array")
    version         = Column(Integer, default=1, comment="审核流程版本")
    ext_prop        = Column(JSON, comment="附加规则字段，供扩展使用")
    status          = Column(Enum('0', '1', name="e_fr_status"), default='1', comment="审批流程是否启用")
    create_tm       = Column(DateTime, default=datetime.now)


class TblFlowJob(Base):
    __tablename__ = "karuo_flow_job"

    id              = Column(Integer, primary_key=True, autoincrement=True)
    flow_id         = Column(Integer, ForeignKey("karuo_flow.id"), comment="审批规则编号")
    catalog         = Column(String(128), nullable=False, comment="审批类型，冗余记录")
    apply_user      = Column(String(128), nullable=False, comment="申请人编号")
    reviewer        = Column(JSON, comment="当前阶段的审核人编号")
    submit_tm       = Column(DateTime, default=datetime.now, comment="提出申请时间")
    closed          = Column(Enum('0', '1', name="e_fj_closed"), default='0', comment="流程是否结束")
    recalled        = Column(Enum('0', '1', name="e_fj_recall"), default='0', comment="是否由发起人撤回")
    close_tm        = Column(DateTime, comment="流程结束时间")
    result          = Column(Enum('0', '1', name="e_fj_result"), default='0', comment="流程结果， 0：未通过；1：通过")

    FlowRule        = relationship("TblFlowRule", foreign_keys=[flow_id])

    def TurnClosed(self):
        self.closed = '1'
        self.close_tm = datetime.now()

class TblFlowRecords(Base):
    __tablename__ = "karuo_flow_records"

    id              = Column(Integer, primary_key=True, autoincrement=True)
    flow_id         = Column(Integer, ForeignKey("karuo_flow.id"), index=True, comment="审批规则编号")
    job_id          = Column(Integer, ForeignKey("karuo_flow_job.id"), index=True, comment="申请单号")
    userid          = Column(String(128), nullable=False, comment="用户编号")
    submit_tm       = Column(DateTime, default=datetime.now, comment="提交时间")
    decision        = Column(Enum('0', '1', name="e_fr_decision"), default='0', comment="决策结果")
    description     = Column(TEXT, default='', comment="备注")

    Job             = relationship("TblFlowJob", foreign_keys=[job_id], backref="flow_list")
    FlowRule        = relationship("TblFlowRule", foreign_keys=[flow_id])

def InitKaruoflowTables(session):
    """
    初始化数据表
    """
    from karuoflow.datadef import DbConfig
    from karuoflow.db.session import createDbSession
    from sqlalchemy.schema import CreateTable
    sess = createDbSession(DbConfig('218.89.168.173', 'duoneng', 'root', 'Net.info.2006'), True)
    print("开始初始化 karuoflow 数据表")
    for table in list(Base.metadata.tables.values()):
        if not session.bind.has_table(table.name):
            create_expr = CreateTable(table)
            sess.execute(create_expr)
            print(f"{table.name} 创建成功")
        else:
            print(f"{table.name} 已经存在")
    return True


if "__main__" == __name__:
    InitKaruoflowTables(None)