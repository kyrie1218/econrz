# China Family Panel Studies
## Baseline samples
[@(China Family Panel Studies) (中国家庭追踪调查, CFPS)](https://www.isss.pku.edu.cn/cfps/index.htm)is implemented by the China Social Science Survey Center of Peking University. Since the completion of the national baseline survey in 2010, as of November 2022, the survey data has been released in 6 rounds of official versions, with each round spaced 2 years apart, i.e. the latest official version is CFPS2020[^1].

The basic units of @(CFPS) is individuals. They are sampled by the method of **implicit stratification with multi-stage probability sampling**. Specifically, in the first stage, 25 provinces[^2] are selected into 6 groups to represent geographic characteristics of the mainland China. 176 Units of county/district of these provinces are separately sampled as primary sampling units (**PSU**). In the second stage, 2511 communities are refined to the 1439. And 640 refined communities are sampled from PSUs. In the third stage, 19986 households are sampled from selected communities. The probability of sampling at all stages considers population size of potential samples. All family members related with these households are potential respondents. A family member is an individual with economic and biological/marital/adoptive dependence on other members. After cleaning up raw responses, **33596 adults and 8990 children in 635 communities** completed the baseline survey. Details information about baseline sampling can be referred to official [CFPS user guide](https://www.isss.pku.edu.cn/cfps/docs/20210511113545661703.pdf). 

## Follow-up samples
CFPS is a longitutional dataset at the family level and shows the rise and fall of baseline families in China. Therefore, any member in baseline and its extended family have a lifetime follow-up survey. According to [CFPS technical document](https://www.isss.pku.edu.cn/cfps/docs/20180927132843624299.pdf), all family members in baseline wave are tagged as "Gene member". If a gene member is at home, he/she is assigned with a self-reported individial questionaire, otherwise a proxied questionaire. In the second wave, if a new family member is a new-born baby or an adopted children aged below 10 of gene members, she/he will be also tagged as a "gene". Also, if a new member is a direct relative (parents, spouse, children excluding new gene members) of gene members, she/he is tagged as a "core". Only gene and core members will be followed with a individual survey. Whether a member is as gene or core relates to the qualification of the further follow-up. Gene members will be unconditionally tracked for life but core members is tracked only when binding to the family of gene members. Note that the individual follow-up study will be temporarily suspended under special conditions such as members in prison, army, abroad, or becoming a monk.

## Survey sequence 
In CFPS, main interests are shared family characteristics and individual information of members and are realized by three types of questionaires: **Family member questionaire**, **family economic questionaire**, and **individual questionaire**. 




[^1]: The released CFPS2020 in Nov, 2022 is experimental and only includes the personal information about child proxy and adult.  

[^2]: 26 provinces in CFPS include Shanghai(上海), Liaoning(辽宁), Henan(河南), Gansu(甘肃), Guangdong(广东), Jiangsu(江苏), Zhejiang(浙江), Fujian(福建), Jiangxi(江西), Anhui(安徽), Shandong(山东), Hebei(河北), Shanxi(山西), Jilin(吉林), Heilongjiang(黑龙江), Guangxi(广西), Hubei(湖北), Hunan(湖南), Sichuan(四川), Guizhou(贵州), Yunnan(云南), Tianjin(天津), Beijing(北京), Chongqing(重庆), Shaanxi(陕西).   



