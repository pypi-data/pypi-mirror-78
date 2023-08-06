# -*- coding: utf-8 -*-
"""
本模块功能：期权定价理论理论计算函数包
所属工具包：证券投资分析工具SIAT 
SIAT：Security Investment Analysis Tool
创建日期：2020年7月16日
最新修订日期：2020年8月5日
作者：王德宏 (WANG Dehong, Peter)
作者单位：北京外国语大学国际商学院
作者邮件：wdehong2000@163.com
版权所有：王德宏
用途限制：仅限研究与教学使用，不可商用！商用需要额外授权。
特别声明：作者不对使用本工具进行证券投资导致的任何损益负责！
"""
#==============================================================================
#统一屏蔽一般性警告
import warnings; warnings.filterwarnings("ignore")    
#==============================================================================
def bs_call(S0,X,Days,r0,sigma,printout=True):
    """
    功能：计算无红利支付的欧式期权B-S定价模型，看涨期权
    注意：
    S0：标的物资产的当前价格，X为其行权价
    sigma：标的物资产价格的年化标准差
    r0：年化无风险利率（需要转化为连续计算的无风险利率）
    Days：距离到期日的天数，需要转换为距离到期日的年数=距离到期日的天数/365
    """
    from scipy import log,exp,sqrt,stats
    #Days为距离到期日的日历日天数
    T=Days/365.
    r=log(r0+1)
    
    d1=(log(S0/X)+(r+sigma*sigma/2.)*T)/(sigma*sqrt(T))
    d2=d1-sigma*sqrt(T)
    
    C0=S0*stats.norm.cdf(d1)-X*exp(-r*T)*stats.norm.cdf(d2)
    
    if not printout: return C0
    print("\n***** Black-Scholes Option Pricing *****")
    print("  For European Style without Dividend")
    print("Assets strike price        :",X)
    print("Asset current price        :",S0)
    print("Annualized price volatility:",round(sigma,4))    
    print("Time to mature in year(s)  :",round(T,2))
    print("Continuously risk-free rate:",round(r,4)*100,'\b%')
    print("Call option price expected :",round(C0,2))
    
    return C0
    
if __name__=='__main__':
    S0=40
    X=42
    Days=183
    r0=0.03
    sigma=0.02
    C0=bs_call(40,42,183,0.015,0.02)

#==============================================================================
def bsm_call(S0,X,Days,r0,sigma,Days1=0,div1=0,printout=True):
    """
    功能：计算有红利支付的欧式期权B-S定价模型，看涨期权
    注意：
    S0：标的物资产的当前价格，X为其行权价
    sigma：标的物资产价格的年化标准差
    r0：年化无风险利率（需要转化为连续计算的无风险利率）
    Days：距离到期日的天数，需要转换为距离到期日的年数=距离到期日的天数/365
    Days1：红利发放时距离到期日的天数，需要转换为年数
    div1：红利金额
    """
    from scipy import log,exp
    #Days1为距离到期日的日历日天数
    T=Days/365.
    T1=Days1/365.
    r=log(r0+1)    
    #调整标的物当前价
    S=S0-exp(-r*T1)*div1
    
    #调用BS模型计算
    C=bs_call(S,X,Days,r0,sigma,printout=False)

    if not printout: return C
    print("\n** Black-Scholes-Merton Option Pricing **")
    print("    For European Style with Dividend")
    print("Assets strike price         :",X)
    print("Asset current price         :",S0)
    print("Annualized price volatility :",round(sigma,4))    
    print("Time to mature in year(s)   :",round(T,2))
    print("Continuously risk-free rate :",round(r,4)*100,'\b%')    
    print("Dividend @ mature in year(s):",div1,"@",round(T1,2))
    print("Call option price expected  :",round(C,2))
    
    return C
    
if __name__=='__main__':
    S0=42
    X=40
    Days=183
    r0=0.03
    sigma=0.02
    dv1=1.5
    Days1=183
    C=bsm_call(42,40,183,0.015,0.02,183,1.5)
    C0=bsm_call(42,40,183,0.015,0.23)

#==============================================================================
def bs_put(S0,X,Days,r0,sigma,printout=True):
    """
    功能：计算无红利支付的欧式期权B-S定价模型，看跌期权
    注意：
    S0：标的物资产的当前价格，X为其行权价
    sigma：标的物资产价格的年化标准差
    r0：年化无风险利率（需要转化为连续计算的无风险利率）
    Days：距离到期日的天数，需要转换为距离到期日的年数=距离到期日的天数/365
    """
    from scipy import log,exp,sqrt,stats
    #Days为距离到期日的日历日天数
    T=Days/365.
    r=log(r0+1)
    
    d1=(log(S0/X)+(r+sigma*sigma/2.)*T)/(sigma*sqrt(T))
    d2=d1-sigma*sqrt(T)
    
    P0=-S0*stats.norm.cdf(-d1)+X*exp(-r*T)*stats.norm.cdf(-d2)

    if not printout: return P0
    print("\n***** Black-Scholes Option Pricing *****")
    print("  For European Style without Dividend")
    print("Assets strike price        :",X)
    print("Asset current price        :",S0)
    print("Annualized price volatility:",round(sigma,4))    
    print("Time to mature in year(s)  :",round(T,2))
    print("Continuously risk-free rate:",round(r,4)*100,'\b%')
    print("Put option price expected  :",round(P0,2))
    
    return P0
    
if __name__=='__main__':
    S0=40
    X=42
    Days=183
    r0=0.03
    sigma=0.02
    P0=bs_put(40,42,183,0.015,0.02)    

#==============================================================================
def bsm_put(S0,X,Days,r0,sigma,Days1=0,div1=0,printout=True):
    """
    功能：计算有红利支付的欧式期权B-S定价模型，看跌期权
    注意：
    S0：标的物资产的当前价格，X为其行权价
    sigma：标的物资产价格的年化标准差
    r0：年化无风险利率（需要转化为连续计算的无风险利率）
    Days：距离到期日的天数，需要转换为距离到期日的年数=距离到期日的天数/365
    Days1：红利发放时距离到期日的天数，需要转换为年数
    div1：红利金额
    """
    from scipy import log,exp,sqrt
    #Days为距离到期日的日历日天数
    T=Days/365.
    T1=Days1/365.
    r=log(r0+1)
    
    S=S0-exp(-r*T1)*div1
    
    #调用BS模型计算
    P=bs_put(S,X,Days,r0,sigma,printout=False)

    if not printout: return P
    print("\n** Black-Scholes-Merton Option Pricing **")
    print("    For European Style with Dividend")
    print("Assets strike price         :",X)
    print("Asset current price         :",S0)
    print("Annualized price volatility :",round(sigma,4))    
    print("Time to mature in year(s)   :",round(T,2))
    print("Continuously risk-free rate :",round(r,4)*100,'\b%')
    print("Dividend @ mature in year(s):",div1,"@",round(T1,2))
    print("Put option price expected   :",round(P,2))
    
    return P
    
if __name__=='__main__':
    S0=42
    X=40
    Days=183
    r0=0.03
    sigma=0.02
    P=bsm_put(42,40,183,0.015,0.23,90,1.5)   
    P0=bsm_put(42,40,183,0.015,0.23)

#==============================================================================
def bsm_put_aprice(Srange,X,Days,r0,sigma,Days1=0,div1=0,graph=True):
    """
    功能：计算有红利支付的欧式期权BSM定价模型，看跌期权，当前价格为变化范围
    注意：
    Srange：标的物资产的当前价格范围，默认20等分后作为横轴绘图
    X：期权的行权价
    sigma：标的物资产价格的年化标准差
    r0：年化无风险利率（需要转化为连续计算的无风险利率）
    Days：距离到期日的天数，需要转换为距离到期日的年数=距离到期日的天数/365
    Days1：红利发放时距离到期日的天数，需要转换为年数
    div1：红利金额
    """
    #通用修改点
    trange=Srange
    #检查是否为列表
    if not isinstance(trange,list):
        print("#Error(bsm_put_aprice): target is not a range,",trange)
        return
    if len(trange) < 2:
        print("#Error(bsm_put_aprice): not enough range for target,",trange)
        return        
    
    #确定起始位置和间隔大小
    tstart=trange[0]; tend=trange[1]
    if len(trange) >=3: tstep=trange[2]    
    else: tstep=(tend-tstart)/20.
    #横轴点列表
    import numpy as np
    tlist=np.arange(tstart,tend+tstep,tstep)

    #循环计算各点数值
    import pandas as pd
    df=pd.DataFrame(columns=['Option Price','Asset Price','Strike Price', \
                             'Days to Maturity','Annual RF', \
                             'Annual Sigma','Div to Maturity','Dividend'])
    for t in tlist:
        #通用修改点
        op=bsm_put(t,X,Days,r0,sigma,Days1,div1,printout=False)
        s=pd.Series({'Option Price':op,'Asset Price':t,'Strike Price':X, \
                     'Days to Maturity':Days,'Annual RF':r0, \
                     'Annual Sigma':sigma,'Div to Maturity':Days1, \
                     'Dividend':div1})
        df=df.append(s,ignore_index=True)        
    #通用修改点
    df2=df.set_index(['Asset Price'])  
    if not graph: return df2      
    
    #绘图
    #通用修改点
    colname='Option Price'; collabel='看跌期权'
    ylabeltxt='期权价格'
    titletxt='期权价格的变化趋势图'
    #通用修改点
    fn1='标的物市场价格'
    fn2='\n[期权信息]行权价='+str(X)+', 距离到期天数='+str(Days)
    fn3='\n年化无风险利率%='+str(round(r0*100.,2))+', 年化波动率%='+str(round(sigma*100.,2))
    if div1==0:
        fn4='\n本产品无红利收益'
    else:
        fn4='\n发放红利时间距离到期天数='+str(div1)+', 红利='+str(div1)
    footnote=fn1+fn2+fn3+fn4
    plot_line(df2,colname,collabel,ylabeltxt,titletxt,footnote)
    
    return df2
    
if __name__=='__main__':
    Srange=[30,50,1]
    X=40
    Days=183
    r0=0.03
    sigma=0.02
    Days1=0
    div1=0
    pdf=bsm_put_aprice(Srange,40,183,0.015,0.23,90,1.5)    

#==============================================================================
def bsm_call_aprice(Srange,X,Days,r0,sigma,Days1=0,div1=0,graph=True):
    """
    功能：计算有红利支付的欧式期权BSM定价模型，看涨期权，当前价格为变化范围
    注意：
    Srange：标的物资产的当前价格范围，默认20等分后作为横轴绘图
    X：期权的行权价
    sigma：标的物资产价格的年化标准差
    r0：年化无风险利率（需要转化为连续计算的无风险利率）
    Days：距离到期日的天数，需要转换为距离到期日的年数=距离到期日的天数/365
    Days1：红利发放时距离到期日的天数，需要转换为年数
    div1：红利金额
    """
    #通用修改点
    trange=Srange
    #检查是否为列表
    if not isinstance(trange,list):
        print("#Error(bsm_call_aprice): target is not a range,",trange)
        return
    if len(trange) < 2:
        print("#Error(bsm_call_aprice): not enough range for target,",trange)
        return        
    
    #确定起始位置和间隔大小
    tstart=trange[0]; tend=trange[1]
    if len(trange) >=3: tstep=trange[2]    
    else: tstep=(tend-tstart)/20.
    #横轴点列表
    import numpy as np
    tlist=np.arange(tstart,tend+tstep,tstep)

    #循环计算各点数值
    import pandas as pd
    df=pd.DataFrame(columns=['Option Price','Asset Price','Strike Price', \
                             'Days to Maturity','Annual RF', \
                             'Annual Sigma','Div to Maturity','Dividend'])
    for t in tlist:
        #通用修改点
        op=bsm_call(t,X,Days,r0,sigma,Days1,div1,printout=False)
        s=pd.Series({'Option Price':op,'Asset Price':t,'Strike Price':X, \
                     'Days to Maturity':Days,'Annual RF':r0, \
                     'Annual Sigma':sigma,'Div to Maturity':Days1, \
                     'Dividend':div1})
        df=df.append(s,ignore_index=True)        
    #通用修改点
    df2=df.set_index(['Asset Price'])  
    if not graph: return df2      
    
    #绘图
    #通用修改点
    colname='Option Price'; collabel='看涨期权'
    ylabeltxt='期权价格'
    titletxt='期权价格的变化趋势图'
    #通用修改点
    fn1='标的物市场价格'
    fn2='\n[期权信息]行权价='+str(X)+', 距离到期天数='+str(Days)
    fn3='\n年化无风险利率%='+str(round(r0*100.,2))+', 年化波动率%='+str(round(sigma*100.,2))
    if div1==0:
        fn4='\n本产品无红利收益'
    else:
        fn4='\n发放红利时间距离到期天数='+str(div1)+', 红利='+str(div1)
    footnote=fn1+fn2+fn3+fn4
    plot_line(df2,colname,collabel,ylabeltxt,titletxt,footnote)
    
    return df2
    
if __name__=='__main__':
    Srange=[30,50,1]
    X=40
    Days=183
    r0=0.03
    sigma=0.02
    Days1=0
    div1=0
    cdf=bsm_call_aprice(Srange,40,183,0.015,0.23,90,1.5)    

#==============================================================================
def bsm_aprice(Srange,X,Days,r0,sigma,Days1=0,div1=0,graph=True):
    """
    功能：计算有红利支付的欧式期权BSM定价模型，看涨/看跌期权，当前价格为变化范围
    注意：
    Srange：标的物资产的当前价格范围，默认20等分后作为横轴绘图
    X：期权的行权价
    sigma：标的物资产价格的年化标准差
    r0：年化无风险利率（需要转化为连续计算的无风险利率）
    Days：距离到期日的天数，需要转换为距离到期日的年数=距离到期日的天数/365
    Days1：红利发放时距离到期日的天数，需要转换为年数
    div1：红利金额
    """
    #通用修改点
    trange=Srange
    #检查是否为列表
    if not isinstance(trange,list):
        print("#Error(bsm_aprice): target is not a range,",trange)
        return
    if len(trange) < 2:
        print("#Error(bsm_aprice): not enough range for target,",trange)
        return        
    
    #看涨期权
    df1=bsm_call_aprice(Srange,X,Days,r0,sigma,Days1=0,div1=0,graph=False)
    #看跌期权
    df2=bsm_put_aprice(Srange,X,Days,r0,sigma,Days1=0,div1=0,graph=False)     
    
    #绘图
    #通用修改点
    ticker1='看涨期权'; colname1='Option Price'; label1='期权-C-'+str(X)
    ticker2='看跌期权'; colname2='Option Price'; label2='期权-P-'+str(X)
    ylabeltxt='期权价格'
    titletxt='期权价格的变化趋势图'
    #通用修改点
    fn1='标的物市场价格-->'
    fn2='\n[期权信息]行权价='+str(X)+', 距离到期天数='+str(Days)
    fn3='\n年化无风险利率%='+str(round(r0*100.,2))+', 年化波动率%='+str(round(sigma*100.,2))
    if div1==0:
        fn4='\n本产品无红利收益'
    else:
        fn4='\n发放红利时间距离到期天数='+str(div1)+', 红利='+str(div1)
    footnote=fn1+fn2+fn3+fn4
    plot_line2_coaxial(df1,ticker1,colname1,label1, \
                       df2,ticker2,colname2,label2, \
                    ylabeltxt,titletxt,footnote)
    return
    
if __name__=='__main__':
    Srange=[30,50,1]
    X=40
    Days=183
    r0=0.03
    sigma=0.02
    Days1=0
    div1=0
    bsm_aprice(Srange,40,183,0.015,0.23,90,1.5)  
    bsm_aprice([30,50],40,183,0.015,0.23,90,1.5)  

#==============================================================================
def bsm_put_maturity(S0,X,Dayrange,r0,sigma,Days1=0,div1=0,graph=True):
    """
    功能：计算有红利支付的欧式期权BSM定价模型，看跌期权，距离到期日天数为变化范围
    注意：
    S0：标的物资产的当前价格
    X：期权的行权价
    sigma：标的物资产价格的年化标准差
    r0：年化无风险利率（需要转化为连续计算的无风险利率）
    Dayrange：距离到期日的天数范围，默认变化间隔为20分之一取整
    Days1：红利发放时距离到期日的天数，需要转换为年数
    div1：红利金额
    """
    #通用修改点
    trange=Dayrange
    #检查是否为列表
    if not isinstance(trange,list):
        print("#Error(bsm_put_maturity): target is not a range,",trange)
        return
    if len(trange) < 2:
        print("#Error(bsm_put_maturity): not enough range for target,",trange)
        return        
    
    #确定起始位置和间隔大小
    tstart=int(trange[0]); tend=int(trange[1])
    if len(trange) >=3: tstep=trange[2]    
    else: tstep=int((tend-tstart)/20)
    #横轴点列表
    #import numpy as np
    tlist=range(tstart,tend+tstep,tstep)

    #循环计算各点数值
    import pandas as pd
    df=pd.DataFrame(columns=['Option Price','Asset Price','Strike Price', \
                             'Days to Maturity','Annual RF', \
                             'Annual Sigma','Div to Maturity','Dividend'])
    for t in tlist:
        #通用修改点
        op=bsm_put(S0,X,t,r0,sigma,Days1,div1,printout=False)
        s=pd.Series({'Option Price':op,'Asset Price':S0,'Strike Price':X, \
                     'Days to Maturity':t,'Annual RF':r0, \
                     'Annual Sigma':sigma,'Div to Maturity':Days1, \
                     'Dividend':div1})
        df=df.append(s,ignore_index=True)        
    #通用修改点
    df2=df.set_index(['Days to Maturity'])  
    if not graph: return df2      
    
    #绘图
    #通用修改点
    colname='Option Price'; collabel='看跌期权'
    ylabeltxt='期权价格'
    titletxt='期权价格的变化趋势图'
    #通用修改点
    fn1='<--距离到期日的天数'
    fn2='\n[期权信息]行权价='+str(X)+', 标的物市价='+str(S0)
    fn3='\n年化无风险利率%='+str(round(r0*100.,2))+', 年化波动率%='+str(round(sigma*100.,2))
    if div1==0:
        fn4='\n本产品无红利收益'
    else:
        fn4='\n发放红利时间距离到期天数='+str(div1)+', 红利='+str(div1)
    footnote=fn1+fn2+fn3+fn4
    plot_line(df2,colname,collabel,ylabeltxt,titletxt,footnote)
    
    return df2
    
if __name__=='__main__':
    S0=42
    X=40
    Dayrange=[200,50]
    r0=0.015
    sigma=0.23
    Days1=90
    div1=1.5
    pdf=bsm_put_maturity(42,40,[200,50],0.015,0.23,90,1.5)    

#==============================================================================
def bsm_call_maturity(S0,X,Dayrange,r0,sigma,Days1=0,div1=0,graph=True):
    """
    功能：计算有红利支付的欧式期权BSM定价模型，看涨期权，距离到期日天数为变化范围
    注意：
    S0：标的物资产的当前价格
    X：期权的行权价
    sigma：标的物资产价格的年化标准差
    r0：年化无风险利率（需要转化为连续计算的无风险利率）
    Dayrange：距离到期日的天数范围，默认变化间隔为20分之一取整
    Days1：红利发放时距离到期日的天数，需要转换为年数
    div1：红利金额
    """
    #通用修改点
    trange=Dayrange
    #检查是否为列表
    if not isinstance(trange,list):
        print("#Error(bsm_call_maturity): target is not a range,",trange)
        return
    if len(trange) < 2:
        print("#Error(bsm_call_maturity): not enough range for target,",trange)
        return        
    
    #确定起始位置和间隔大小
    tstart=int(trange[0]); tend=int(trange[1])
    if len(trange) >=3: tstep=trange[2]    
    else: tstep=int((tend-tstart)/20)
    #横轴点列表
    #import numpy as np
    tlist=range(tstart,tend+tstep,tstep)

    #循环计算各点数值
    import pandas as pd
    df=pd.DataFrame(columns=['Option Price','Asset Price','Strike Price', \
                             'Days to Maturity','Annual RF', \
                             'Annual Sigma','Div to Maturity','Dividend'])
    for t in tlist:
        #通用修改点
        op=bsm_call(S0,X,t,r0,sigma,Days1,div1,printout=False)
        s=pd.Series({'Option Price':op,'Asset Price':S0,'Strike Price':X, \
                     'Days to Maturity':t,'Annual RF':r0, \
                     'Annual Sigma':sigma,'Div to Maturity':Days1, \
                     'Dividend':div1})
        df=df.append(s,ignore_index=True)        
    #通用修改点
    df2=df.set_index(['Days to Maturity'])  
    if not graph: return df2      
    
    #绘图
    #通用修改点
    colname='Option Price'; collabel='看涨期权'
    ylabeltxt='期权价格'
    titletxt='期权价格的变化趋势图'
    #通用修改点
    fn1='<--距离到期日的天数'
    fn2='\n[期权信息]行权价='+str(X)+', 标的物市价='+str(S0)
    fn3='\n年化无风险利率%='+str(round(r0*100.,2))+', 年化波动率%='+str(round(sigma*100.,2))
    if div1==0:
        fn4='\n本产品无红利收益'
    else:
        fn4='\n发放红利时间距离到期天数='+str(div1)+', 红利='+str(div1)
    footnote=fn1+fn2+fn3+fn4
    plot_line(df2,colname,collabel,ylabeltxt,titletxt,footnote)
    
    return df2
    
if __name__=='__main__':
    S0=42
    X=40
    Dayrange=[200,50]
    r0=0.015
    sigma=0.23
    Days1=90
    div1=1.5
    cdf=bsm_call_maturity(42,40,[200,50],0.015,0.23,90,1.5)    

#==============================================================================
def bsm_maturity(S0,X,Dayrange,r0,sigma,Days1=0,div1=0,graph=True):
    """
    功能：计算有红利支付的欧式期权BSM定价模型，看涨/看跌期权，距离到期日天数为变化范围
    注意：
    S0：标的物资产的当前价格
    X：期权的行权价
    sigma：标的物资产价格的年化标准差
    r0：年化无风险利率（需要转化为连续计算的无风险利率）
    Dayrange：距离到期日的天数范围，默认间隔为20分之一取证
    Days1：红利发放时距离到期日的天数，需要转换为年数
    div1：红利金额
    """
    #通用修改点
    trange=Dayrange
    #检查是否为列表
    if not isinstance(trange,list):
        print("#Error(bsm_maturity): target is not a range,",trange)
        return
    if len(trange) < 2:
        print("#Error(bsm_maturity): not enough range for target,",trange)
        return        
    
    #看涨期权
    df1=bsm_call_maturity(S0,X,Dayrange,r0,sigma,Days1=0,div1=0,graph=False)
    df1.sort_index(ascending=True, inplace=True)
    #看跌期权
    df2=bsm_put_maturity(S0,X,Dayrange,r0,sigma,Days1=0,div1=0,graph=False)
    df2.sort_index(ascending=True, inplace=True)  
    #合并
    import pandas as pd
    df=pd.merge(df1,df2,how='inner',left_index=True,right_index=True,sort=True)
    
    #绘图
    import matplotlib.pyplot as plt
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False     
    
    plt.title('期权价格的变化趋势图')
    plt.ylabel('期权价格')
    
    df['Option Price_x'].plot(label='看涨期权',ls='-')
    df['Option Price_y'].plot(label='看跌期权',ls='-.')
    
    fn1='<--距离到期日的天数'
    fn2='\n[期权信息]行权价='+str(X)+', 标的物市价='+str(S0)
    fn3='\n年化无风险利率%='+str(round(r0*100.,2))+', 年化波动率%='+str(round(sigma*100.,2))
    if div1==0: fn4='\n本产品无红利收益'
    else: fn4='\n发放红利时间距离到期天数='+str(div1)+', 红利='+str(div1)
    footnote=fn1+fn2+fn3+fn4
    plt.xlabel(footnote)  
    
    plt.legend()
    plt.show()    
    
    return
    
if __name__=='__main__':
    S0=42
    X=40
    Dayrange=[200,50]
    r0=0.015
    sigma=0.23
    Days1=90
    div1=1.5
    bsm_maturity(S0,40,[200,5],0.015,0.23,90,1.5)  
    bsm_maturity(42,40,[50,200],0.015,0.23,90,1.5)  

#==============================================================================
def bsm_put_sigma(S0,X,Days,r0,sigmarange,Days1=0,div1=0,graph=True):
    """
    功能：计算有红利支付的欧式期权BSM定价模型，看跌期权，年化波动率为变化范围
    注意：
    S0：标的物资产的当前价格
    X：期权的行权价
    sigmarange：标的物资产价格的年化标准差范围，默认为区间的20分之一作为间隔
    r0：年化无风险利率（需要转化为连续计算的无风险利率）
    Days：距离到期日的天数
    Days1：红利发放时距离到期日的天数，需要转换为年数
    div1：红利金额
    """
    #通用修改点
    trange=sigmarange
    #检查是否为列表
    if not isinstance(trange,list):
        print("#Error(bsm_put_sigma): target is not a range,",trange)
        return
    if len(trange) < 2:
        print("#Error(bsm_put_sigma): not enough range for target,",trange)
        return        
    
    #确定起始位置和间隔大小
    tstart=trange[0]; tend=trange[1]
    if len(trange) >=3: tstep=trange[2]    
    else: tstep=(tend-tstart)/20.
    #横轴点列表
    import numpy as np
    tlist=np.arange(tstart,tend+tstep,tstep)

    #循环计算各点数值
    import pandas as pd
    df=pd.DataFrame(columns=['Option Price','Asset Price','Strike Price', \
                             'Days to Maturity','Annual RF', \
                             'Annual Sigma','Div to Maturity','Dividend'])
    for t in tlist:
        #通用修改点
        op=bsm_put(S0,X,Days,r0,t,Days1,div1,printout=False)
        s=pd.Series({'Option Price':op,'Asset Price':S0,'Strike Price':X, \
                     'Days to Maturity':Days,'Annual RF':r0, \
                     'Annual Sigma':t,'Div to Maturity':Days1, \
                     'Dividend':div1})
        df=df.append(s,ignore_index=True)        
    #通用修改点
    df2=df.set_index(['Annual Sigma'])  
    if not graph: return df2      
    
    #绘图
    #通用修改点
    colname='Option Price'; collabel='看跌期权'
    ylabeltxt='期权价格'
    titletxt='期权价格的变化趋势图'
    #通用修改点
    fn1='波动率-->'
    fn2='\n[期权信息]行权价='+str(X)+', 标的物市价='+str(S0)
    fn3='\n年化无风险利率%='+str(round(r0*100.,2))+', 距离到期日天数='+str(Days)
    if div1==0:
        fn4='\n本产品无红利收益'
    else:
        fn4='\n发放红利时间距离到期天数='+str(div1)+', 红利='+str(div1)
    footnote=fn1+fn2+fn3+fn4
    plot_line(df2,colname,collabel,ylabeltxt,titletxt,footnote)
    
    return df2
    
if __name__=='__main__':
    S0=42
    X=40
    Days=183
    r0=0.015
    sigmarange=[0.1,0.4]
    Days1=90
    div1=1.5
    pdf=bsm_put_sigma(42,40,183,0.015,[0.1,0.4],90,1.5)    


#==============================================================================
def bsm_call_sigma(S0,X,Days,r0,sigmarange,Days1=0,div1=0,graph=True):
    """
    功能：计算有红利支付的欧式期权BSM定价模型，看涨期权，年化波动率为变化范围
    注意：
    S0：标的物资产的当前价格
    X：期权的行权价
    sigmarange：标的物资产价格的年化标准差范围，默认为区间的20分之一作为间隔
    r0：年化无风险利率（需要转化为连续计算的无风险利率）
    Days：距离到期日的天数
    Days1：红利发放时距离到期日的天数，需要转换为年数
    div1：红利金额
    """
    #通用修改点
    trange=sigmarange
    #检查是否为列表
    if not isinstance(trange,list):
        print("#Error(bsm_call_sigma): target is not a range,",trange)
        return
    if len(trange) < 2:
        print("#Error(bsm_call_sigma): not enough range for target,",trange)
        return        
    
    #确定起始位置和间隔大小
    tstart=trange[0]; tend=trange[1]
    if len(trange) >=3: tstep=trange[2]    
    else: tstep=(tend-tstart)/20.
    #横轴点列表
    import numpy as np
    tlist=np.arange(tstart,tend+tstep,tstep)

    #循环计算各点数值
    import pandas as pd
    df=pd.DataFrame(columns=['Option Price','Asset Price','Strike Price', \
                             'Days to Maturity','Annual RF', \
                             'Annual Sigma','Div to Maturity','Dividend'])
    for t in tlist:
        #通用修改点
        op=bsm_call(S0,X,Days,r0,t,Days1,div1,printout=False)
        s=pd.Series({'Option Price':op,'Asset Price':S0,'Strike Price':X, \
                     'Days to Maturity':Days,'Annual RF':r0, \
                     'Annual Sigma':t,'Div to Maturity':Days1, \
                     'Dividend':div1})
        df=df.append(s,ignore_index=True)        
    #通用修改点
    df2=df.set_index(['Annual Sigma'])  
    if not graph: return df2      
    
    #绘图
    #通用修改点
    colname='Option Price'; collabel='看涨期权'
    ylabeltxt='期权价格'
    titletxt='期权价格的变化趋势图'
    #通用修改点
    fn1='波动率-->'
    fn2='\n[期权信息]行权价='+str(X)+', 标的物市价='+str(S0)
    fn3='\n年化无风险利率%='+str(round(r0*100.,2))+', 距离到期日天数='+str(Days)
    if div1==0:
        fn4='\n本产品无红利收益'
    else:
        fn4='\n发放红利时间距离到期天数='+str(div1)+', 红利='+str(div1)
    footnote=fn1+fn2+fn3+fn4
    plot_line(df2,colname,collabel,ylabeltxt,titletxt,footnote)
    
    return df2
    
if __name__=='__main__':
    S0=42
    X=40
    Days=183
    r0=0.015
    sigmarange=[0.1,0.4]
    Days1=90
    div1=1.5
    cdf=bsm_call_sigma(42,40,183,0.015,[0.1,0.4],90,1.5)  

#==============================================================================
def bsm_sigma(S0,X,Days,r0,sigmarange,Days1=0,div1=0,graph=True):
    """
    功能：计算有红利支付的欧式期权BSM定价模型，看涨/看跌期权，波动率为变化范围
    注意：
    S0：标的物资产的当前价格
    X：期权的行权价
    sigmarange：标的物资产价格的年化标准差范围
    r0：年化无风险利率（需要转化为连续计算的无风险利率）
    Days：距离到期日的天数
    Days1：红利发放时距离到期日的天数，需要转换为年数
    div1：红利金额
    """
    #通用修改点
    trange=sigmarange
    #检查是否为列表
    if not isinstance(trange,list):
        print("#Error(bsm_sigma): target is not a range,",trange)
        return
    if len(trange) < 2:
        print("#Error(bsm_sigma): not enough range for target,",trange)
        return        
    
    #看涨期权
    df1=bsm_call_sigma(S0,X,Days,r0,sigmarange,Days1=0,div1=0,graph=False)
    df1.sort_index(ascending=True, inplace=True)
    #看跌期权
    df2=bsm_put_sigma(S0,X,Days,r0,sigmarange,Days1=0,div1=0,graph=False)
    df2.sort_index(ascending=True, inplace=True)  
    
    #绘制双线图
    titletxt='期权价格的变化趋势图'
    colname1='Option Price'; label1='看涨期权'
    colname2='Option Price'; label2='看跌期权'
    ylabeltxt='期权价格'
    
    fn1='波动率-->'
    fn2='\n[期权信息]行权价='+str(X)+', 标的物市价='+str(S0)
    fn3='\n年化无风险利率%='+str(round(r0*100.,2))+', 距离到期日天数='+str(Days)
    if div1==0: fn4='\n本产品无红利收益'
    else: fn4='\n发放红利时间距离到期天数='+str(div1)+', 红利='+str(div1)
    footnote=fn1+fn2+fn3+fn4
    
    plot_2lines(df1,colname1,label1,df2,colname2,label2, \
                ylabeltxt,titletxt,footnote)
    
    return
    
if __name__=='__main__':
    S0=42
    X=40
    Days=183
    r0=0.015
    sigmarange=[0.1,0.4]
    Days1=90
    div1=1.5
    bsm_sigma(42,40,183,0.015,[0.1,0.4],90,1.5)  

#==============================================================================
def iv_call_bsm(aop,S0,X,Days,r0,Days1=0,div1=0,precision=0.01,printout=True):
    """
    功能：基于BSM模型，二分迭代法，计算隐含波动率，看涨期权
    aop：实际期权价格
    S0：标的物当前市价
    X：标的物行权价
    Days：距离到期日的天数
    r0：年华无风险利率
    Days1：预期红利收益发放日期距离到期日的天数，默认=0
    div1：预期红利收益金额，默认=0
    printout：是否显示计算结果，默认=True
    """
    k=1
    volLow=0.001    #设置波动率的最低值
    volHigh=1.0     #设置波动率的最高值
    
    #波动率最低值对应的期权价格
    #cLow=bsCall(S,X,T,r,volLow)
    cLow=bsm_call(S0,X,Days,r0,volLow,Days1,div1,printout=False)
    
    #波动率最高值对应的期权价格
    #cHigh=bsCall(S,X,T,r,volHigh)  
    cHigh=bsm_call(S0,X,Days,r0,volHigh,Days1,div1,printout=False)
    
    #防止出现死循环
    if cLow > aop or cHigh < aop: 
        print("#Error(iv_call_bsm): Option price not reasonable,",aop)
        return None        
        #raise ValueError    
    
    while k ==1:
        #cLow=bsCall(S,X,T,r,volLow)
        cLow=bsm_call(S0,X,Days,r0,volLow,Days1,div1,printout=False)
        #cHigh=bsCall(S,X,T,r,volHigh)
        cHigh=bsm_call(S0,X,Days,r0,volHigh,Days1,div1,printout=False)
        
        #取波动率的高低均值
        volMid=(volLow+volHigh)/2.0
        #cMid=bsCall(S,X,T,r,volMid) 
        cMid=bsm_call(S0,X,Days,r0,volMid,Days1,div1,printout=False)
        
        #满足期权价格误差精度要求（0.01以下）则结束循环
        if abs(cHigh-cLow) < precision: k=2
        #否则，缩小范围，继续循环
        elif cMid>aop: volHigh=volMid
        else: volLow=volMid        
    
    iv=round(volMid,4)
    if not printout: return iv
    
    #显示
    print("\n*** Implied Volatility: Binomial Iteration ***")
    print("Call option:")
    print("  Actual option price     :",aop)
    print("  Current price of assets :",S0)
    print("  Exercise price of assets:",X)
    print("  To maturity in day(s)   :",Days)
    if not (div1 == 0):
        print("  Dividend expected             :",div1)
        print("  Dividend to maturity in day(s):",Days1)
    print("Implied volatility:")
    print("  Estimated annualized volatility :",iv)
    print("  Corresponding option price range:",round(cLow,3),'-',round(cHigh,3))
    print("  Iteration precision             :",precision)
    return iv

#==============================================================================
def iv_put_bsm(aop,S0,X,Days,r0,Days1=0,div1=0,precision=0.01,printout=True):
    """
    功能：基于BSM模型，二分迭代法，计算隐含波动率，看跌期权
    aop：实际期权价格
    S0：标的物当前市价
    X：标的物行权价
    Days：距离到期日的天数
    r0：年华无风险利率
    Days1：预期红利收益发放日期距离到期日的天数，默认=0
    div1：预期红利收益金额，默认=0
    printout：是否显示计算结果，默认=True
    """
    k=1
    volLow=0.001    #设置波动率的最低值
    volHigh=1.0     #设置波动率的最高值
    
    #波动率最低值对应的期权价格
    #cLow=bsCall(S,X,T,r,volLow)
    cLow=bsm_put(S0,X,Days,r0,volLow,Days1,div1,printout=False)
    
    #波动率最高值对应的期权价格
    #cHigh=bsCall(S,X,T,r,volHigh)  
    cHigh=bsm_put(S0,X,Days,r0,volHigh,Days1,div1,printout=False)
    
    #防止出现死循环
    if cLow > aop or cHigh < aop: 
        print("#Error(iv_put_bsm): Option price not reasonable,",aop)
        return None
        #raise ValueError    
    
    while k ==1:
        #cLow=bsCall(S,X,T,r,volLow)
        cLow=bsm_put(S0,X,Days,r0,volLow,Days1,div1,printout=False)
        #cHigh=bsCall(S,X,T,r,volHigh)
        cHigh=bsm_put(S0,X,Days,r0,volHigh,Days1,div1,printout=False)
        
        #取波动率的高低均值
        volMid=(volLow+volHigh)/2.0
        #cMid=bsCall(S,X,T,r,volMid) 
        cMid=bsm_put(S0,X,Days,r0,volMid,Days1,div1,printout=False)
        
        #满足期权价格误差精度要求（precision）则结束循环
        if abs(cHigh-cLow) < precision: k=2
        #否则，缩小范围，继续循环
        elif cMid>aop: volHigh=volMid
        else: volLow=volMid        
    
    iv=round(volMid,4)
    if not printout: return iv
    
    #显示
    print("\n*** Implied Volatility: Binomial Iteration ***")
    print("Put option:")
    print("  Actual option price     :",aop)
    print("  Current price of assets :",S0)
    print("  Exercise price of assets:",X)
    print("  To maturity in day(s)   :",Days)
    if not (div1 == 0):
        print("  Dividend expected             :",div1)
        print("  Dividend to maturity in day(s):",Days1)
    print("Implied volatility:")
    print("  Estimated annualized volatility :",iv)
    print("  Corresponding option price range:",round(cLow,3),'-',round(cHigh,3))
    print("  Iteration precision             :",precision)

    return iv

#==============================================================================
def binomial_american_call(S0,X,Days,r0,sigma,q0=0,steps=200,printout=True):
    """
    功能：计算有红利支付的美式期权二叉树定价模型，看涨期权
    注意：
    S0：标的物资产的当前价格
    X为其行权价
    Days：距离到期日的天数，需要转换为距离到期日的年数=距离到期日的天数/365
    r0：年化无风险利率（需要转化为连续计算的无风险利率）
    sigma：标的物资产价格的年化标准差
    q0：年化红利收益率，由于美式期权可能提前行权，故不考虑发放日期
    steps：二叉树的步骤
    """
    from scipy import log,exp
    #Days1为距离到期日的日历日天数
    t=Days/365.
    r=log(r0+1)  
    q=log(q0+1)
    #调整标的物当前价
    S=S0    

    import numpy as np
    u=np.exp(sigma*np.sqrt(t/steps)); d=1/u
	
    P=(np.exp((r-q)*t/steps)-d)/(u-d)
    prices=np.zeros(steps+1)
    c_values=np.zeros(steps+1)
    prices[0]=S*d**steps
    c_values[0]=np.maximum(prices[0]-X,0)
	
    for i in range(1,steps+1):
        prices[i]=prices[i-1]*(u**2)
        c_values[i]=np.maximum(prices[i]-X,0)
	
    for j in range(steps,0,-1):
        for i in range(0,j):
            prices[i]=prices[i+1]*d
            #c_values[i]=np.maximum((P*c_values[i+1]+(1-P)*c_values[i])/np.exp(r*t/steps),prices[i]-X)
            c_values[i]=np.maximum((P*c_values[i+1]+(1-P)*c_values[i])/np.exp((r-q)*t/steps),prices[i]-X)
    C=round(c_values[0],2)

    if not printout: return C
    print("\n***** Binomial Option Pricing *****")
    print("  For American Style with Dividend")
    print("Assets strike price        :",X)
    print("Asset current price        :",S0)
    print("Annualized price volatility:",round(sigma,4))    
    print("Time to mature in year(s)  :",round(t,2))
    print("Continuously risk-free rate:",round(r,4)*100,'\b%')
    print("Continuously dividend rate :",round(q,4)*100,'\b%')
    print("Binomial tree steps used   :",steps)
    print("Call option price expected :",round(C,2))    
    
    return C

#==============================================================================
def binomial_american_put(S0,X,Days,r0,sigma,q0=0,steps=200,printout=True):
    """
    功能：计算有红利支付的美式期权二叉树定价模型，看跌期权
    注意：
    S0：标的物资产的当前价格
    X为其行权价
    Days：距离到期日的天数，需要转换为距离到期日的年数=距离到期日的天数/365
    r0：年化无风险利率（需要转化为连续计算的无风险利率）
    sigma：标的物资产价格的年化标准差
    q0：年化红利收益率，由于美式期权可能提前行权，故不考虑发放日期
    steps：二叉树的步骤
    """
    from scipy import log,exp
    #Days1为距离到期日的日历日天数
    t=Days/365.
    r=log(r0+1)  
    q=log(q0+1)
    #调整标的物当前价
    S=S0   
    
    import numpy as np
    u=np.exp(sigma*np.sqrt(t/steps))
    d=1/u
    P=(np.exp((r-q)*t/steps)-d)/(u-d)
    prices=np.zeros(steps+1)
    c_values=np.zeros(steps+1)
    prices[0]=S*d**steps
    c_values[0]=np.maximum(X-prices[0],0)

    for i in range(1,steps+1):
        prices[i]=prices[i-1]*(u**2)
        c_values[i]=np.maximum(X-prices[i],0)

    for j in range(steps,0,-1):
        for i in range(0,j):
            prices[i]=prices[i+1]*d
            #c_values[i]=np.maximum((P*c_values[i+1]+(1-P)*c_values[i])/np.exp(r*t/steps),X-prices[i])#检查是否提前行权
            c_values[i]=np.maximum((P*c_values[i+1]+(1-P)*c_values[i])/np.exp((r-q)*t/steps),X-prices[i])#检查是否提前行权
    C=round(c_values[0],2)

    if not printout: return C
    print("\n***** Binomial Option Pricing *****")
    print("  For American Style with Dividend")
    print("Assets strike price        :",X)
    print("Asset current price        :",S0)
    print("Annualized price volatility:",round(sigma,4))    
    print("Time to mature in year(s)  :",round(t,2))
    print("Continuously risk-free rate:",round(r,4)*100,'\b%')
    print("Continuously dividend rate :",round(q,4)*100,'\b%')
    print("Binomial tree steps used   :",steps)
    print("Put option price expected  :",round(C,2)) 

    return C

#==============================================================================


#==============================================================================
#==============================================================================
#==============================================================================
#==============================================================================
#==============================================================================
#==============================================================================    
def plot_line(df,colname,collabel,ylabeltxt,titletxt,footnote,datatag=False, \
              power=0,zeroline=False):
    """
    功能：绘制折线图。如果power=0不绘制趋势图，否则绘制多项式趋势图
    假定：数据表有索引，且已经按照索引排序
    输入：数据表df，数据表中的列名colname，列名的标签collabel；y轴标签ylabeltxt；
    标题titletxt，脚注footnote；是否在图中标记数据datatag；趋势图的多项式次数power
    输出：折线图
    返回值：无
    """
    import matplotlib.pyplot as plt
    
    #设置绘图时的汉字显示
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False  

    #先绘制折线图
    plt.plot(df.index,df[colname],'-',label=collabel, \
             linestyle='-',linewidth=2,color='blue', \
                 marker='o',markersize=2)
    #绘制数据标签
    if datatag:
        for x, y in zip(df.index, df[colname]):
            plt.text(x,y+0.1,'%.2f' % y,ha='center',va='bottom',color='black')        
    
    #是否绘制水平0线
    if zeroline and (min(df[colname]) < 0):
        plt.axhline(y=0,ls=":",c="black")
        
    #绘制趋势线
    if power > 0:
        try:
            #生成行号，借此将横轴的日期数量化，以便拟合
            df['id']=range(len(df))
        
            #设定多项式拟合，power为多项式次数
            import numpy as np
            parameter = np.polyfit(df.id, df[colname], power)
            f = np.poly1d(parameter)
            plt.plot(df.index, f(df.id),"r--", label="趋势线")
        except: pass
    
    plt.legend(loc='best')
    plt.gcf().autofmt_xdate() # 优化标注（自动倾斜）
    #plt.xticks(rotation=45)
    plt.ylabel(ylabeltxt)
    plt.xlabel(footnote)
    plt.title(titletxt,fontsize=12)
    plt.show()
    plt.close()
    return

if __name__ =="__main__":
    plot_line(df,'Close',"收盘价","价格","万科股票","数据来源：雅虎财经",power=4)

#==============================================================================
def plot_2lines(df1,colname1,label1,df2,colname2,label2, \
                ylabeltxt,titletxt,footnote,hline=0,vline=0):
    """
    功能：绘制两个证券的折线图。如果hline=0不绘制水平虚线，vline=0不绘制垂直虚线
    假定：数据表有索引，且已经按照索引排序
    输入：
    证券1：数据表df1，列名1，列名标签1；
    证券2：数据表df2，列名2，列名标签2；
    标题titletxt，脚注footnote
    输出：绘制同轴折线图
    返回值：无
    """
    import matplotlib.pyplot as plt
    #设置绘图时的汉字显示
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False 
    plt.title(titletxt,fontsize=12)
    
    #证券1：先绘制折线图
    plt.plot(df1.index,df1[colname1],label=label1,linestyle='-',linewidth=2)
    
    #证券2：先绘制折线图
    plt.plot(df2.index,df2[colname2],label=label2,linestyle='-.',linewidth=2)
    """
    #是否绘制水平虚线
    if not (hline == 0):
        plt.axhline(y=hline,ls=":",c="black")
    #是否绘制垂直虚线
    if not (vline == 0):
        plt.axvline(x=vline,ls=":",c="black")
    """    
    plt.ylabel(ylabeltxt)
    plt.xlabel(footnote)
    plt.legend(loc='best')
    plt.show()
    
    return

if __name__ =="__main__":
    df1=bsm_call_maturity(42,40,[50,200],0.015,0.23,90,1.5)
    df2=bsm_put_maturity(42,40,[50,200],0.015,0.23,90,1.5)
    ticker1='A'; colname1='Option Price'; label1='A1'
    ticker2='B'; colname2='Option Price'; label2='B2'
    ylabeltxt='ylabel'; titletxt='title'; footnote='\n\n\n\n4lines'
    power=0; datatag1=False; datatag2=False; zeroline=False
    
#==============================================================================
def plot_line2_coaxial(df1,ticker1,colname1,label1, \
                       df2,ticker2,colname2,label2, \
                    ylabeltxt,titletxt,footnote, \
                    power=0,datatag1=False,datatag2=False,zeroline=False):
    """
    功能：绘制两个证券的折线图。如果power=0不绘制趋势图，否则绘制多项式趋势图
    假定：数据表有索引，且已经按照索引排序
    输入：
    证券1：数据表df1，证券代码ticker1，列名1，列名标签1；
    证券2：数据表df2，证券代码ticker2，列名2，列名标签2；
    标题titletxt，脚注footnote；是否在图中标记数据datatag；趋势图的多项式次数power
    输出：绘制同轴折线图
    返回值：无
    """
 
    import matplotlib.pyplot as plt
    #设置绘图时的汉字显示
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置默认字体
    plt.rcParams['axes.unicode_minus'] = False 
    plt.title(titletxt,fontsize=12)
    
    #证券1：先绘制折线图
    plt.plot(df1.index,df1[colname1],label=codetranslate(ticker1)+'('+label1+')', \
             linestyle='-',linewidth=2)
    #证券1：绘制数据标签
    if datatag1:
        for x, y in zip(df1.index, df1[colname1]):
            plt.text(x,y+0.1,'%.2f' % y,ha='center',va='bottom',color='black')        
    #绘证券1：制趋势线
    if power > 0:
        try:
            #生成行号，借此将横轴的日期数量化，以便拟合
            df1['id']=range(len(df1))
            #设定多项式拟合，power为多项式次数
            import numpy as np
            parameter = np.polyfit(df1.id, df1[colname1], power)
            f = np.poly1d(parameter)
            plt.plot(df1.index, f(df1.id),"r--", label=codetranslate(ticker1)+"(趋势线)")
        except: pass
    
    #证券2：先绘制折线图
    plt.plot(df2.index,df2[colname2],label=codetranslate(ticker2)+'('+label2+')', \
             linestyle='-.',linewidth=2)
    #证券2：绘制数据标签
    if datatag2:
        for x, y in zip(df2.index, df2[colname2]):
            plt.text(x,y+0.1,'%.2f' % y,ha='center',va='bottom',color='black')        
    #绘证券2：趋势线
    if power > 0:
        try:
            #生成行号，借此将横轴的日期数量化，以便拟合
            df2['id']=range(len(df2))
            #设定多项式拟合，power为多项式次数
            import numpy as np
            parameter = np.polyfit(df2.id, df2[colname2], power)
            f = np.poly1d(parameter)
            plt.plot(df2.index, f(df2.id),"r--", label=codetranslate(ticker2)+"(趋势线)")
        except: pass

    #是否绘制水平0线
    if zeroline and ((min(df1[colname1]) < 0) or (min(df2[colname2]) < 0)):
        plt.axhline(y=0,ls=":",c="black")
    
    plt.legend(loc='best')
    plt.ylabel(ylabeltxt)
    plt.xlabel(footnote)
    plt.gcf().autofmt_xdate() # 优化标注（自动倾斜）    
    plt.show()
    
    return

if __name__ =="__main__":
    df1=bsm_call_maturity(42,40,[50,200],0.015,0.23,90,1.5)
    df2=bsm_put_maturity(42,40,[50,200],0.015,0.23,90,1.5)
    ticker1='A'; colname1='Option Price'; label1='A1'
    ticker2='B'; colname2='Option Price'; label2='B2'
    ylabeltxt='ylabel'; titletxt='title'; footnote='\n\n\n\n4lines'
    power=0; datatag1=False; datatag2=False; zeroline=False

#==============================================================================
def codetranslate(code):
    """
    翻译证券代码为证券名称。
    输入：证券代码。输出：证券名称
    """
    import pandas as pd
    codedict=pd.DataFrame([
        ['000002.SZ','万科地产A股'],['600266.SS','北京城建A股'],
        ['600519.SS','茅台酒A股'],['601398.SS','工商银行A股'],
        ['601939.SS','建设银行A股'],['601288.SS','农业银行A股'],
        ['601988.SS','中国银行A股'],['601857.SS','中国石油A股'],
        ['000651.SZ','格力电器A股'],['000333.SZ','美的集团A股'],
        
        ['AAPL','苹果'],['MSFT','微软'],['AMZN','亚马逊'],['JD','京东'],
        ['FB','脸书'],['BABA','阿里巴巴美股'],['PTR','中石油美股'],
        ['ZM','ZOOM'],['C','花旗集团'],['F','福特汽车'],['GOOG','谷歌'],
        ['KO','可口可乐'],['PEP','百事可乐'],['IBM','国际商用机器'],
        ['HPQ','惠普'],['BA','波音'],['GM','通用汽车'],['INTC','英特尔'],
        ['AMD','超威半导体'],['NVDA','英伟达'],['PFE','辉瑞制药'],
        ['BILI','哔哩哔哩'],['TAL','好未来'],['EDU','新东方'],['VIPS','唯品会'],
        ['SINA','新浪网'],['BIDU','百度'],['NTES','网易'],['PDD','拼多多'],
        ['COST','好事多'],['WMT','沃尔玛'],['DIS','迪士尼'],['GS','高盛'],
        ['QCOM','高通'],['BAC','美国银行'],
        ['JPM','摩根大通'],['WFC','富国银行'],['GS','高盛集团'],['MS','摩根示丹利'],
        ['USB','美国合众银行'],['TD','道明银行'],['PNC','PNC金融'],['BK','纽约梅隆银行'],
        
        ['0700.HK','港股腾讯控股'],['9988.HK','阿里巴巴港股'],
        ['1810.HK','港股小米'],['0992.HK','港股联想'],['1398.HK','工商银行港股'],
        ['0939.HK','建设银行港股'],['1288.HK','农业银行港股'],
        ['3988.HK','中国银行港股'],['0857.HK','中国石油港股'],
        ['0005.HK','港股汇丰控股'],['2888.HK','港股渣打银行'],
        
        ['6758.T','日股索尼'],['4911.T','日股资生堂'],['8306.T','三菱日联金融'],
        ['7203.T','日股丰田汽车'],['7267.T','日股本田汽车'],
        ['7201.T','日股日产汽车'],['8411.T','日股瑞穗金融'],['7182.T','日本邮政银行'],
        
        ['TCS.NS','印度股塔塔咨询'],['005930.KS','韩股三星电子'],
        ['UBSG.SW','瑞士股瑞银'],['UG.PA','法国股标致雪铁龙'],
        ['DAI.DE','德国股奔驰汽车'],
        ['BMW.DE','德国股宝马汽车']
        ], columns=['code','codename'])

    try:
        codename=codedict[codedict['code']==code]['codename'].values[0]
    except:
        #未查到翻译词汇，返回原词
        codename=code
   
    return codename

if __name__=='__main__':
    code='GOOG'
    print(codetranslate('000002.SZ'))
    print(codetranslate('9988.HK'))

#==============================================================================#==============================================================================
#==============================================================================#==============================================================================
#==============================================================================
#==============================================================================
def option_maturity(ticker):
    """
    功能：获得期权的各个到期日期
    """
    import yfinance as yf
    opt = yf.Ticker(ticker)
    
    #获得期权的各个到期日
    try:
        exp_dates=opt.options
    except:
        print("#Error(option_maturity): no option available for",ticker)
        return None
    
    #显示结果
    print("\n***** Option Maturity Dates *****")
    print("Underlying assets:",ticker)
    datelist=list(exp_dates)
    print("Maturity dates   :")
    
    num=len(datelist)
    for d in datelist:
        print(d,end='  ')
        pos=datelist.index(d)+1
        if (pos % 4 ==0) or (pos==num): print(' ')
    
    print("Total number     :",num,"dates.")
    import datetime
    today = datetime.date.today()    
    print("*** Source: Yahoo Finance,",today)
    
    return datelist

if __name__=='__main__':
    ticker='AAPL'
    datelist=option_maturity(ticker)
    datelist=option_maturity('AAPL')
    datelist=option_maturity('000001.SS')

#================================================================
def option_chain(ticker,mdate):
    """
    功能：获得期权的各个到期日期，并列出某个到期日的期权合约
    """
    import yfinance as yf
    opt = yf.Ticker(ticker)
            
    #处理称为规范日期
    from datetime import datetime
    mdate2 = datetime.strptime(mdate, '%Y-%m-%d')
    mdate3 = datetime.strftime(mdate2,'%Y-%m-%d')

    import datetime
    today = datetime.date.today()    
    
    #获得一个到期日的所有期权合约
    try:
        optlist = opt.option_chain(mdate3)
    except:
        print("#Error(option_chain): no option available for",ticker,'\b@',mdate)
        return None    
    
    opt_call=optlist.calls
    opt_call['underlyingAsset']=ticker
    opt_call['optionType']='Call'
    opt_call['date']=today
    opt_call['maturity']=mdate3
    
    collist=['contractSymbol','underlyingAsset','optionType','date', \
             'maturity','strike','lastPrice','impliedVolatility', \
             'inTheMoney','currency']
    opt_call2=opt_call[collist].copy()
    num_call=len(opt_call2)
    num_call_ITM=len(opt_call2[opt_call2['inTheMoney']==True])
    num_call_OTM=num_call-num_call_ITM
    
    strike_min=min(opt_call2['strike'])
    strike_max=max(opt_call2['strike'])
    currency=opt_call2['currency'][0]
    
    opt_put=optlist.puts
    opt_put['underlyingAsset']=ticker
    opt_put['optionType']='Put'
    opt_put['date']=today
    opt_put['maturity']=mdate3
    opt_put2=opt_put[collist].copy()
    num_put=len(opt_put2)
    num_put_ITM=len(opt_put2[opt_put2['inTheMoney']==True])
    num_put_OTM=num_put-num_put_ITM
    
    print("\n***** Option Chain *****")
    print("Underlying asset  :",ticker)
    print("Maturity date     :",mdate)
    print("Call options      :",num_call)
    print("  In/Out the money:",num_call_ITM,'/',num_call_OTM)
    print("Put options       :",num_put)
    print("  In/Out the money:",num_put_ITM,'/',num_put_OTM)
    print("Min/Max strike    :",strike_min,'/',strike_max,currency)
    
    import datetime
    today = datetime.date.today()    
    print("*** Source: Yahoo Finance,",today)
    
    #绘图
    df1=opt_call2.copy()
    df1.sort_values(by=['strike'],axis=0,ascending=[True],inplace=True) 
    df1.set_index(['strike'],inplace=True)
    colname1='lastPrice'; label1='Call Price'
    
    df2=opt_put2.copy()
    df2.sort_values(by=['strike'],axis=0,ascending=[True],inplace=True) 
    df2.set_index(['strike'],inplace=True)
    colname2='lastPrice'; label2='Put Price'  
    
    ylabeltxt='Option Price('+currency+')'
    titletxt="Option Price: Implication of Strike Price"
    footnote="Strike Price("+currency+") -->\n"+ \
        "Underlying asset: "+ticker+ \
        ", "+"Maturity: "+mdate+ \
        "\nSource: Yahoo Finance, "+str(today)
    plot_2lines(df1,colname1,label1,df2,colname2,label2, \
                ylabeltxt,titletxt,footnote)    
    
    return  opt_call2, opt_put2

if __name__=='__main__':
    ticker='AAPL'    
    mdate='2022-6-17'    
    dfc,dfp=option_chain(ticker,mdate)
