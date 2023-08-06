# -*- encoding: utf-8 -*-
'''
@文件    :flowapp.py
@说明    :
@时间    :2020/09/02 14:27:13
@作者    :caimmy@hotmail.com
@版本    :0.1
'''
from datetime import datetime
from .db.tables import TblFlowJob, TblFlowRule, TblFlowRecords
from sqlalchemy import and_
from .error_code import KaruoFlowErrors

class FlowModelsAgent():
    def __init__(self, db_session):
        self.db = db_session


    def RefuseJobFlow(self, job_id:int, user_id:str, reason:str):
        """
        拒绝一项审批
        job_id: 
        user_id
        """
        ret_code = KaruoFlowErrors.ERR_UNKOWN
        job_item = self.db.query(TblFlowJob).get(job_id)
        if job_item:
            current_flow = self.db.query(TblFlowRule).get(job_item.flow_id)
            try:
                if user_id in current_flow.reviewer:
                    # 关闭审批任务
                    job_item.result = '0'
                    job_item.TurnClosed()
                    # 追加审批流
                    job_item.flow_list.append(TblFlowRecords(
                        flow_id= job_item.flow_id,
                        job_id = job_id,
                        userid = user_id,
                        submit_tm = datetime.now(),
                        decision = '0',
                        description = reason
                    ))
                    self.db.commit()
                    ret_code = KaruoFlowErrors.SUCCESS
                else:
                    ret_code = KaruoFlowErrors.ERR_FLOW_OWNER_INVALID
            except Exception as e:
                self.db.rollback()
                ret_code = KaruoFlowErrors.ERR_DB_EXCEPTION
        return ret_code

    def AgreeJobFlow(self, job_id:int, user_id:str, reason:str):
        """
        通过一项审批流程
        """
        ret_code = KaruoFlowErrors.ERR_UNKOWN

        job_item = self.db.query(TblFlowJob).get(job_id)
        if job_item:
            current_flow = self.db.query(TblFlowRule).get(job_item.flow_id)
            next_flow = self.db.query(TblFlowRule).filter(TblFlowRule.prev_id==job_item.flow_id).one_or_none()
        
            if user_id in current_flow.reviewer:
                try:
                    flow_record = TblFlowRecords(
                        flow_id = job_item.flow_id,
                        job_id = job_item.id,
                        userid = user_id,
                        submit_tm = datetime.now(),
                        decision = '1',
                        description = reason
                    )
                    job_item.flow_list.append(flow_record)
                    if next_flow:
                        # 流程尚未结束，需要往下一阶段路由
                        # 更新审批任务，添加路由节点
                        job_item.flow_id = next_flow.id 
                        job_item.reviewer = next_flow.reviewer
                    else:
                        job_item.TurnClosed()
                        # 设置审批任务为通过
                        job_item.result = '1'
                    self.db.commit()
                    ret_code = KaruoFlowErrors.SUCCESS
                except Exception as e:
                    print(e)
                    ret_code = KaruoFlowErrors.ERR_DB_EXCEPTION
            else:
                ret_code = KaruoFlowErrors.ERR_FLOW_OWNER_INVALID
        return ret_code

    def NextFlowNode(self, flow_id:int):
        """
        获取下一个流程节点
        """
        next_flow_node = self.db.query(TblFlowRule).filter(
            and_(
                TblFlowRule.prev_id==flow_id,
                TblFlowRule.status=='1'
            )
        ).one_or_none()
        return next_flow_node


    