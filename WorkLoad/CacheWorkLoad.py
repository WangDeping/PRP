import pandas as pd
from CacheFactory import CacheFactory
from IWorkLoad import IWorkLoad


class CacheWorkLoad(IWorkLoad):
    """所有从Cache中提取的工作量"""

    def __init__(self, timeperoid):
        super(CacheWorkLoad, self).__init__(timeperoid)
        self.db = CacheFactory()

        pass

    #住院执行工作量
    def IPExeWorkLoad(self):
        #queryTxt = "SELECT oeore_rowid,oeore_oeori_ParREF->oeori_userdepartment_dr->ctloc_desc,oeore_oeori_ParREF->OEORI_OEORD_ParRef->OEORD_Adm_DR->PAadm_PAPMI_DR->PAPMI_NO,OEORE_OEORI_ParRef->OEORI_ItmMast_DR->ARCIM_Desc,OEORE_OEORI_ParRef->OEORI_PHFreq_DR->PHCFR_Code,OEORE_ExStDate,OEORE_CTPCP_DR->CTPCP_Code,OEORE_CTPCP_DR->CTPCP_Desc,OEORE_OEORI_ParRef->OEORI_phqtyord,OEORE_OEORI_ParRef->oeori_durat_dr->phcdu_desc1 FROM OE_OrdExec WHERE OEORE_Order_Status_DR=1 AND OEORE_ExStDate BETWEEN '" + self.timeperoid[0] + "' and '" + self.timeperoid[1] + "' AND OEORE_OEORI_ParRef->OEORI_ItmMast_DR->ARCIM_ItemCat_DR->ARCIC_OrdCat_DR IN ('2','3','4','5','6','10','12','14','15','16','24','25','107','108')"
        queryTxt="SELECT oeore_rowid,oeore_oeori_ParREF->oeori_userdepartment_dr->ctloc_desc,oeore_oeori_ParREF->OEORI_OEORD_ParRef->OEORD_Adm_DR->PAadm_PAPMI_DR->PAPMI_NO,OEORE_OEORI_ParRef->OEORI_ItmMast_DR->ARCIM_Desc,OEORE_OEORI_ParRef->OEORI_PHFreq_DR->PHCFR_Code,OEORE_ExStDate,OEORE_CTPCP_DR->CTPCP_Code,OEORE_CTPCP_DR->CTPCP_Desc,OEORE_OEORI_ParRef->OEORI_phqtyord,OEORE_OEORI_ParRef->oeori_durat_dr->phcdu_desc1,OEORE_OEORI_ParRef->oeori_priority_dr->oecpr_desc,OEORE_OEORI_ParRef->oeori_doctor_dr->ctpcp_code,OEORE_OEORI_ParRef->oeori_doctor_dr->ctpcp_desc,OEORE_OEORI_ParRef->oeori_useradd->SSUSR_Initials,OEORE_OEORI_ParRef->oeori_useradd->SSUSR_Name FROM OE_OrdExec WHERE OEORE_Order_Status_DR=1 AND OEORE_ExStDate BETWEEN '" + self.timeperoid[0] + "' and '" + self.timeperoid[1] + "' AND OEORE_OEORI_ParRef->OEORI_ItmMast_DR->ARCIM_ItemCat_DR->ARCIC_OrdCat_DR IN ('2','3','4','5','6','10','12','14','15','16','24','25','107','108')"
        result = self.db.exequery(queryTxt)
        data = pd.DataFrame.from_records(result, columns=self.exe_columns)
        return data
        pass

    #门诊执行工作量
    def OPExeWorkLoad(self):
        queryTxt = "SELECT oeore_rowid,oeore_oeori_ParREF->oeori_recdep_dr->ctloc_desc,oeore_oeori_ParREF->OEORI_OEORD_ParRef->OEORD_Adm_DR->PAadm_PAPMI_DR->PAPMI_NO,OEORE_OEORI_ParRef->OEORI_ItmMast_DR->ARCIM_Desc,OEORE_OEORI_ParRef->OEORI_PHFreq_DR->PHCFR_Code,TO_CHAR(OEORE_DateExecuted,'YYYY-MM-DD')AS  OEORE_ExStDate,OEORE_CTPCP_DR->CTPCP_Code,OEORE_CTPCP_DR->CTPCP_Desc,OEORE_OEORI_ParRef->OEORI_phqtyord,OEORE_OEORI_ParRef->oeori_durat_dr->phcdu_desc1,OEORE_OEORI_ParRef->oeori_priority_dr->oecpr_desc,OEORE_OEORI_ParRef->oeori_doctor_dr->ctpcp_code,OEORE_OEORI_ParRef->oeori_doctor_dr->ctpcp_desc,OEORE_OEORI_ParRef->oeori_useradd->SSUSR_Initials,OEORE_OEORI_ParRef->oeori_useradd->SSUSR_Name  FROM OE_OrdExec WHERE OEORE_Order_Status_DR=1 AND OEORE_DateExecuted BETWEEN '" + self.timeperoid[0] + "' and '" + self.timeperoid[1] + "' AND OEORE_OEORI_ParRef->OEORI_ItmMast_DR->ARCIM_ItemCat_DR->ARCIC_OrdCat_DR IN ('2','3','4','5','6','10','12','14','15','16','24','25' ) AND ((oeore_oeori_ParREF->oeori_recdep_dr IN ('44')) OR (oeore_oeori_ParREF->oeori_recdep_dr->ctloc_dep_dr='6'))"
        result = self.db.exequery(queryTxt)
        data = pd.DataFrame.from_records(result, columns=self.exe_columns)
        return data
        pass

    def exeWorkLoad(self):
        ip_exeworkload = self.IPExeWorkLoad()  #.to_excel("ip.xlsx")
        op_exeworkload = self.OPExeWorkLoad()  #.to_excel("op.xlsx")
        exeworkload = pd.concat(
            [ip_exeworkload, op_exeworkload], ignore_index=True)
        exeworkload.drop_duplicates([self.exe_columns["执行ID"]], inplace=True)
        #exeworkload.columns=self.exe_columns
        #print("我执行了这一次")
        return exeworkload
        pass

    #手术
    def anaesthesiaWorkLoad(self):
        queryTxt = "CALL web.OperPatInfo('" + self.timeperoid[0] + "','" + self.timeperoid[1] + "')"
        result = self.db.exequery(queryTxt)
        data = pd.DataFrame.from_records(result, columns=self.operation_header)
        return data

    #医嘱开单
    def orderWorkLoad(self):
        queryTxt = "select OEORI_OrdDept_DR->CTLOC_Desc,OEORI_OEORD_ParRef->oeord_adm_dr->paadm_papmi_dr->papmi_no,OEORI_OEORD_ParRef->oeord_adm_dr->paadm_papmi_dr->papmi_name,oeori_doctor_dr->ctpcp_code,oeori_doctor_dr->ctpcp_desc,oeori_useradd->SSUSR_Initials,oeori_useradd->SSUSR_Name,OEORI_ItmMast_DR->arcim_desc,OEORI_Date,oeori_rowid,OEORI_phqtyord,oeori_priority_dr->oecpr_desc  from oe_orditem where OEORI_ItemStat_DR IN ('1','4','6') and  OEORI_Date BETWEEN '" + self.timeperoid[0] + "' and '" + self.timeperoid[1] + "' and OEORI_ItmMast_DR->ARCIM_ItemCat_DR->ARCIC_OrdCat_DR not in ('17','18','19','20','21','22','23','27','28','30')"
        result = self.db.exequery(queryTxt)
        data = pd.DataFrame.from_records(result, columns=self.order_header)
        return data

    #根据用法获取工作量
    def usageExeWorkLoad(self, usagetup):
        queryTxt = "SELECT oeore_rowid,oeore_oeori_ParREF->oeori_userdepartment_dr->ctloc_desc,oeore_oeori_ParREF->OEORI_OEORD_ParRef->OEORD_Adm_DR->PAadm_PAPMI_DR->PAPMI_NO,OEORE_OEORI_ParRef->OEORI_ItmMast_DR->ARCIM_Desc,OEORE_OEORI_ParRef->OEORI_PHFreq_DR->PHCFR_Code,OEORE_OEORI_ParRef->oeori_instr_dr->PHCIN_Desc1,OEORE_ExStDate,OEORE_CTPCP_DR->CTPCP_Code,OEORE_CTPCP_DR->CTPCP_Desc,OEORE_OEORI_ParRef->OEORI_phqtyord,OEORE_OEORI_ParRef->oeori_durat_dr->phcdu_desc1 FROM OE_OrdExec WHERE OEORE_Order_Status_DR=1 AND OEORE_ExStDate BETWEEN '" + self.timeperoid[0] + "' and '" + self.timeperoid[1] + "' AND OEORE_OEORI_ParRef->oeori_instr_dr->PHCIN_Desc1 IN " + usagetup.__str__(
        ) + ""
        result = self.db.exequery(queryTxt)
        data = pd.DataFrame.from_records(result)
        return data
        pass

    #慢病传染病上报卡
    def chronicWorkLoad(self):
        queryTxt = "CALL web.INFECTIONTJ('" + self.timeperoid[0] + "','" + self.timeperoid[1] + "')"
        result = self.db.exequery(queryTxt)
        data = pd.DataFrame.from_records(result)
        return data

    #护理病历记录(一级、二级、危重、新生儿)
    def nurseRecordWorkload(self, type):
        queryTxt = "CALL web.HLDetails('" + self.timeperoid[0] + "','" + self.timeperoid[1] + "','" + type + "')"        
        result = self.db.exequery(queryTxt)
        data = pd.DataFrame.from_records(result)        
        return data
        pass

    #护理病历审核(质控护士)
    def nurseRecordCheckPointsWorkload(self):
        queryTxt = "CALL web.HLSHDetail('" + self.timeperoid[0] + "','" + self.timeperoid[1] + "')"
        result = self.db.exequery(queryTxt)
        data = pd.DataFrame.from_records(result)
        return data
        pass

    #护士处理医嘱
    def nurseOrderHandle(self):
        queryTxt = "CALL web.NurseOrdWork('" + self.timeperoid[0] + "','" + self.timeperoid[1] + "')"
        result = self.db.exequery(queryTxt)
        data = pd.DataFrame.from_records(result)
        return data
        pass

    # 医师查房,按出院日期统计
    def patientRounds(self):
        queryTxt = "CALL web.EPRSignReport('" + self.timeperoid[0] + "','" + self.timeperoid[1] + "')"
        result = self.db.exequery(queryTxt)
        data = pd.DataFrame.from_records(result)
        return data
        pass

# RIS申请单登记统计

    def rislocApplication(self, loc):
        queryTxt = "CALL web.RisLocStatics('" + loc + "','" + self.timeperoid[0] + "','" + self.timeperoid[1] + "')"
        result = self.db.exequery(queryTxt)
        data = pd.DataFrame.from_records(result)
        return data
        pass

# 病案首页:质控医师 科主任
    def homePageInfo(self):
        queryTxt = "CALL  web.WTADMINFO('" + self.timeperoid[0] + "','" + self.timeperoid[1] + "')"
        result = self.db.exequery(queryTxt)
        data = pd.DataFrame.from_records(result)
        return data
        pass
        
# 临床路径统计
    def clinicalPathway(self):
        queryTxt= "CALL  web.ClinicalpathwayNum('" + self.timeperoid[0] + "','" + self.timeperoid[1] + "')"  
        result=self.db.exequery(queryTxt)
        data = pd.DataFrame.from_records(result)
        
        return data
        pass  

# 办理出院结算信息明细
    def dischargePatientsInfo(self):
        queryTxt= "CALL web.QueryCYPATInfo('" + self.timeperoid[0] + "','" + self.timeperoid[1] + "')"  
        result=self.db.exequery(queryTxt)
        data = pd.DataFrame.from_records(result)
        return data
        pass

# 办理入院患者信息明细
    def admissionPatientsInfo(self):
        queryTxt= "CALL web.QueryRYPATInfo('" + self.timeperoid[0] + "','" + self.timeperoid[1] + "')"  
        result=self.db.exequery(queryTxt)
        data = pd.DataFrame.from_records(result)
        return data
        pass
# PACS 检查、报告、审核工作量明细:[INSPECTION,REPORT,VERIFY]
    def pacsWorkload(self,typeOfWork):
        queryTxt="CALL web.YJWorkLoad('" + self.timeperoid[0] + "','" + self.timeperoid[1] + "','"+typeOfWork+"')"
        result=self.db.exequery(queryTxt)
        data = pd.DataFrame.from_records(result)
        return data
        pass
#CALL WEB.NotBillOEORI("2018-03-01","2018-03-10") 督察门诊未结算
#CALL web.GetOEORIQuantity('2018-01-01','2018-05-23','中药熏洗') 根据医嘱名字模糊搜索
