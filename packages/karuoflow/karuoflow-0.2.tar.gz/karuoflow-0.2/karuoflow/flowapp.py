# -*- encoding: utf-8 -*-
'''
@文件    :flowapp.py
@说明    :
@时间    :2020/09/02 14:27:13
@作者    :caimmy@hotmail.com
@版本    :0.1
'''
from dataclasses import dataclass
from sqlalchemy.orm import Session
from sqlalchemy import and_
from .db.session import createDbSession
from .db.tables import TblFlowRule, TblFlowJob, TblFlowRecords
from .flowmodelagent import FlowModelsAgent
from .datadef import DbConfig
from .error_code import KaruoFlowErrors

class KaruoFlow:
    def __init__(self):
        self.db_config = None
        self.db_session = None
        self.flows_agent = None

    @classmethod
    def CreateModel(cls, dbconfig: DbConfig=None, session: Session=None):
        _instance = cls()
        if session:
            # 优先按照session参数实例化类
            _instance.db_session = session
        elif dbconfig:
            # 初始化数据库连接
            _instance.db_session = createDbSession(dbconfig)
        _instance.flows_agent = FlowModelsAgent(_instance.db_session)
        return _instance


    def QueryFlow(self, flow_catalog:str, version:int = 1):
        """
        查询流程
        """
        flow_items = self.db_session.query(TblFlowRule).filter(and_(
            TblFlowRule.catalog == flow_catalog,
            TblFlowRule.version == version,
            TblFlowRule.status == '1'
        )).order_by(TblFlowRule.prev_id.asc()).all()
        return [f.property2Dict() for f in flow_items]

    def QueryLastFlow(self, flow_catalog:str):
        """
        查询最新的流程
        按照version倒序排列
        """
        flow_item = self.db_session.query(TblFlowRule).filter(and_(
            TblFlowRule.catalog==flow_catalog,
            TblFlowRule.status=='1'
        )).order_by(TblFlowRule.version.desc()).limit(1).first()
        return self.QueryFlow(flow_catalog, flow_item.version) if flow_item else []

    def QueryAllEnabledFlowRules(self):
        """
        获取所有可以使用的审批流程
        @return list
        """
        flow_rules = self.db_session.query(TblFlowRule).filter(and_(
            TblFlowRule.prev_id==0,
            TblFlowRule.status=='1',
        )).all()
        return [_flow.property2Dict() for _flow in flow_rules] 

    # ======================= querys

    def _QueryApplySets(self, user_id: str, catalog:str = None, closed_label: str=None):
        """
        根据close字段来查询某个ID作为发起人的审核流程
        catalog: 审批类别
        close_label: 关闭字段内容, ['0', '1']
        """
        _common_query = self.db_session.query(TblFlowJob).filter(TblFlowJob.apply_user==user_id)
        if catalog:
            _common_query.filter(TblFlowJob.catalog==catalog)
        if closed_label and closed_label in ['0', '1']:
            _common_query.filter(TblFlowJob.closed==closed_label)
        return _common_query.order_by(TblFlowJob.id.desc()).all()
        

    def QueryApplyListInDoing(self, user_id, catalog: str=None):
        """
        查询用户发起的正在进行中的审批记录
        """
        return self._QueryApplySets(user_id, catalog, '0')

    def QueryApplyListClosed(self, user_id, catalog: str=None):
        """
        查询用户发起的已经结束的审批记录
        """
        return self._QueryApplySets(user_id, catalog, '1')

    def QueryReviewTodoList(self, user_id, catalog:str=None):
        """
        查询用户正在审批的记录
        """
        _common_query = self.db_session.query(TblFlowJob).filter(and_(
            TblFlowJob.closed=='0',
            TblFlowJob.reviewer.contains(user_id)
        ))
        if catalog:
            _common_query.filter(TblFlowJob.catalog==catalog)
        _common_query.order_by(TblFlowJob.id.desc())
        return _common_query.all()



    # ======================= operations
        
    def Apply(self, catalog: str, userid: str, desc: str, version:int = 1):
        """
        发起流程
        通过流程类别来发起
        """
        job_id = 0
        ret_code = KaruoFlowErrors.ERR_UNKOWN
        flow_item_list = self.db_session.query(TblFlowRule).filter(and_(
            TblFlowRule.catalog == catalog,
            TblFlowRule.version == version,
            TblFlowRule.status == '1'
        )).order_by(TblFlowRule.prev_id.asc()).all()
        flow_item = flow_item_list[0] if len(flow_item_list) > 1 else None
        next_flow = flow_item_list[1]
        # 判断len(flow_item_list) > 1的目的是确保流程的具备审核节点
        if flow_item and flow_item.prev_id == 0 and next_flow.prev_id == flow_item.id:
            # 得到流程的第一个节点
            if not flow_item.reviewer or userid in flow_item.reviewer:
                try:
                    # 首先创建一个任务，然后初始化流程
                    _job = TblFlowJob()
                    _job.flow_id = next_flow.id
                    _job.catalog = catalog
                    _job.apply_user = userid
                    _job.reviewer = next_flow.reviewer
                    self.db_session.add(_job)
                    self.db_session.flush()

                    _record = TblFlowRecords()
                    _record.flow_id = flow_item.id
                    _record.job_id = _job.id
                    _record.userid = userid

                    _record.description = desc
                    self.db_session.add(_record)

                    self.db_session.commit()
                    job_id = _job.id
                    ret_code = KaruoFlowErrors.SUCCESS
                except Exception as e:
                    self.db_session.rollback()
            else:
                ret_code = KaruoFlowErrors.ERR_FLOW_STATUS_INVALID
        else:
            ret_code = KaruoFlowErrors.ERR_DATA_NOT_FOUND
        return ret_code, job_id

    def Recall(self, jobid:int, user_id: str):
        """
        撤回一个审批申请
        1、该申请尚未结束；
        2、该申请是由本人发起
        """
        ret_code = KaruoFlowErrors.ERR_UNKOWN
        _job = self.db_session.query(TblFlowJob).get(jobid)
        if _job:
            if _job.apply_user == user_id:
                if _job.closed == '0':
                    try:
                        _job.recalled = '1'
                        _job.result = '0'
                        _job.TurnClosed()
                        self.db_session.commit()
                        ret_code = KaruoFlowErrors.SUCCESS
                    except Exception as _:
                        self.db_session.rollback()
                        ret_code = KaruoFlowErrors.ERR_DB_EXCEPTION
                else:
                    ret_code = KaruoFlowErrors.ERR_FLOW_CLOSED
            else:
                ret_code = KaruoFlowErrors.ERR_FLOW_OWNER_INVALID
        else:
            ret_code = KaruoFlowErrors.ERR_DATA_NOT_FOUND
        return ret_code

    def Examine(self, jobid:int, user_id:str, agree:bool, desc:str):
        """
        审批一项申请
        :param jobid 申请编号
        :param user_id 审批者编号
        :param agree 通过或拒绝
        :param desc 备注信息
        """
        ret_code = KaruoFlowErrors.ERR_UNKOWN
        apply_job = self.db_session.query(TblFlowJob).get(jobid)
        if apply_job:
            if user_id in apply_job.reviewer:
                if apply_job.closed == '0':
                    if agree:
                        ret_code = self.flows_agent.AgreeJobFlow(jobid, user_id, desc)
                    else:
                        ret_code = self.flows_agent.RefuseJobFlow(jobid, user_id, desc)
                else:
                    ret_code = KaruoFlowErrors.ERR_FLOW_CLOSED
            else:
                ret_code = KaruoFlowErrors.ERR_FLOW_OWNER_INVALID
        else:
            ret_code = KaruoFlowErrors.ERR_DATA_NOT_FOUND
        return ret_code
