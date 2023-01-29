# TidyData

???+ abstract
    `TidyData` is a Python class to tidying up raw data for economic research. And it includes the following functions:

    - `scan_file_path` generates a generator of file paths by scanning a directory. 


## Full codes
=== "Source"
    ```python title="core.py"
    --8<-- "docs/codes/tidydata/sample/core.py"
    ```

=== "Result"
    ```
    child2012
            pid   fid12   fid10  ...    rswt_respn1012 releaseversion interviewerid
    0  110022103  110022  110022  ...  14234.8521131742            5.3         10062
    1  222320401  222320  110020  ...               NaN            5.3         10062
    2  110011105  110011  110011  ...  17737.1652478081            5.3         10062

    [3 rows x 806 columns]
    child2010
            pid     fid    cid  ... mparty releaseversion interviewerid
    0  450307106  450307  10230  ...     群众            5.1            -8
    1  410389106  410389  20810  ...     群众            5.1            -8
    2  450307103  450307  10230  ...     群众            5.1            -8

    [3 rows x 726 columns]
    person2018
            pid code   fid18  ... pg1201_max interviewerid18 releaseversion
    0  100051501  501  100051  ...        NaN          761040            2.1
    1  100051502  502  100051  ...        NaN          761040            2.1
    2  100160601  601  100160  ...        NaN          459505            2.1

    [3 rows x 1371 columns]
    famconf2010
            pid     fid    cid provcd  ... moccupcode moccupisco mparty releaseversion
    0  110001101  110001  11830    北京市  ...        NaN        NaN    NaN            5.1
    1  110001102  110001  11830    北京市  ...        NaN        NaN    NaN            5.1
    2  110002101  110002  11830    北京市  ...  不便分类的其他人群        NaN     群众            5.1

    [3 rows x 370 columns]
    famconf2012
            pid   fid12 fid10 code_a_p  ... feduc12 meduc12 generation releaseversion
    0  100453401  100453   不适用      401  ...     不适用    大学本科        二代户              6
    1  100453401  430111   不适用      401  ...     不适用    大学本科        一代户              6
    2  100453431  100453   不适用      431  ...     不适用     不适用        二代户              6

    [3 rows x 331 columns]
    famroster2011
            pid     fid code  ta1y  ... tb8m tb801 nff501_min_update releaseversion
    0  110001101  110001  101  1972  ...  不适用    -8               不适用            1.1
    1  110001102  110001  102  1970  ...  不适用    -8               不适用            1.1
    2  110003101  110003  101  1971  ...  不适用    -8               不适用            1.1

    [3 rows x 53 columns]
    childproxy2018
            pid   fid18   fid16  ... cfps2018eduy_im interviewerid18 releaseversion
    0  100551552  100551  100551  ...               0          696822            2.1
    1  100724602  100724     不适用  ...               0          163482            2.1
    2  100810601  100810     不适用  ...               0          803368            2.1

    [3 rows x 289 columns]
    famconf2018
        fid18 fid_provcd18 fid_countyid18  ... iwmode18 interviewerid18 releaseversion
    0  100051          北京市             45  ...       电访          761040              1
    1  100051          北京市             45  ...       电访          761040              1
    2  100051          北京市             45  ...       电访          761040              1

    [3 rows x 296 columns]
    adult2010
            pid     fid    cid  ... mparty releaseversion interviewerid
    0  411643103  411643  20950  ...     群众            5.2            -8
    1  310203103  310203  20050  ...     群众            5.2            -8
    2  410285102  410285  20740  ...     群众            5.2            -8

    [3 rows x 1484 columns]
    comm2010
        cid provcd countyid psu  ... cz911 cz912 releaseversion interviewerid
    0  13200    天津市       79  79  ...     7     7            5.1            -8
    1  13190    天津市       79  79  ...     7     7            5.1            -8
    2  12780    山西省       69  69  ...     5     7            5.1            -8

    [3 rows x 224 columns]
    famecon2012
        fid12   fid10 provcd  ...    fswt_respn1012 releaseversion interviewerid
    0  370738  370738    山东省  ...  40144.1421451807            6.1            -8
    1  440449  440449    广东省  ...               NaN            6.1            -8
    2  430026  430026    湖南省  ...  27059.1689638084            6.1            -8

    [3 rows x 622 columns]
    famecon2018
        fid18   fid16   fid14  ... interrupt interviewerid18 releaseversion
    0  100051  100051  100051  ...       NaN          761040            2.2
    1  100160  100160  100160  ...       NaN          459505            2.2
    2  100286  100286  100286  ...       NaN          966285            2.2

    [3 rows x 321 columns]
    child2014
            pid proxyrpt selfrpt  ... cfps2014eduy_im releaseversion interviewerid
    0  210956105        有      没有  ...               4            2.1         10154
    1  441674401        有      没有  ...               0            2.1         10154
    2  130385106        有      没有  ...               0            2.1         10154

    [3 rows x 687 columns]
    famconf2014
        fid14   fid12   fid10 provcd14  ... cyear cmonth kz103 releaseversion
    0  100051     不适用     不适用      北京市  ...  2014      8   普通话            2.0
    1  100051     不适用     不适用      北京市  ...  2014      8   普通话            2.0
    2  100051  110043  110043      北京市  ...  2014      8   普通话            2.0

    [3 rows x 307 columns]
    crossyearid2018
            pid birthy gender  ... coremember18 alive18 releaseversion
    0  100051501   1969      女  ...         核心成员      健在         2018.1
    1  100051502   1966      男  ...         核心成员      健在         2018.1
    2  100160601   1989      男  ...         核心成员      健在         2018.1

    [3 rows x 95 columns]
    famconf2016
        fid16   fid14 fid12 fid10  ... iwmode subpopulation subsample releaseversion
    0  100051  100051   不适用   不适用  ...     电访       其它省市子总体         是            1.0
    1  100051  100051   不适用   不适用  ...     电访       其它省市子总体         是            1.0
    2  100376     不适用   不适用   不适用  ...     电访       其它省市子总体         是            1.0

    [3 rows x 286 columns]
    adult2012
            pid   fid12   fid10  ...    rswt_respn1012 releaseversion interviewerid
    0  370742102  370742  370742  ...  32249.9879691714            6.1            -8
    1  370727101  370727  370727  ...  32423.3580194144            6.1            -8
    2  110013103  110013  110013  ...   25800.058721238            6.1         10062

    [3 rows x 1744 columns]
    child2016
            pid   fid16   fid14  ... cfps2016eduy_im releaseversion interviewerid
    0  211915501  211915  211915  ...               0            2.1         11228
    1  230394103  138434  230394  ...               1            2.1         11228
    2  210254105  210254  210254  ...               0            2.1         11228

    [3 rows x 633 columns]
    famecon2016
        fid16   fid14   fid12  ... fswt_respn1016 familysize16 releaseversion
    0  100051  100051  110043  ...           6975            3            2.0
    1  100160  100160  120009  ...          10430            1            2.0
    2  100286  100286  130005  ...          13785            1            2.0

    [3 rows x 329 columns]
    famecon2014
        fid14   fid12   fid10  ... fswt_respn1014 releaseversion interviewerid
    0  410951  410951  410951  ...            NaN            2.1            -8
    1  135821  520507  520507  ...          27179            2.1         10154
    2  275366  620694  620694  ...            NaN            2.1         10154

    [3 rows x 459 columns]
    adult2016
            pid code_a_p   fid16  ... cfps2016eduy_im releaseversion interviewerid
    0  230384101      101  230384  ...              15            2.2         11228
    1  230052102      102  230052  ...              12            2.2         11228
    2  230364103      103  230364  ...              16            2.2         11228

    [3 rows x 1095 columns]
    adult2011
            pid     fid provcd  ... mathtest11 wordtest11 releaseversion
    0  110033105  110033    北京市  ...         18         32              1
    1  110043107  110043    北京市  ...         18         22              1
    2  110063102  110063    北京市  ...         23         34              1

    [3 rows x 724 columns]
    comm2014
        cid14  cid10 provcd14  ... subsample14 releaseversion interviewerid
    0  118100  11810      北京市  ...           是            2.2         10571
    1  118200  11820      北京市  ...           是            2.2         10571
    2  212300  21230      河南省  ...           是            2.2         10508

    [3 rows x 234 columns]
    famecon2010
        fid    cid provcd countyid  ... mortage expense interviewerid releaseversion
    0  110001  11830    北京市       45  ...       0   37160         11518            5.2
    1  110003  11830    北京市       45  ...       0   96300         11518            5.2
    2  110005  11830    北京市       45  ...     204   18604         11518            5.2

    [3 rows x 663 columns]
    adult2014
            pid   fid14   fid12  ... releaseversion interviewerid_sf interviewerid_pr
    0  441876105  291078  441876  ...            2.2               -8            10817
    1  140093104  140093  140093  ...            2.2               -8            10293
    2  130510104  130510  130510  ...            2.2               -8            10293

    [3 rows x 1191 columns]
    family2011
        fid provcd countyid  ... typecomm urbancomm releaseversion
    0  110001    北京市       45  ...       城市        城镇            1.1
    1  110003    北京市       45  ...       城市        城镇            1.1
    2  110006    北京市       45  ...       城市        城镇            1.1

    [3 rows x 372 columns]
    child2011
            pid     fid provcd  ... mathtest11 wordtest11 releaseversion
    0  110003103  110003    北京市  ...         16         31              1
    1  110011103  110011    北京市  ...         11         25              1
    2  110011104  110011    北京市  ...          8         12              1

    [3 rows x 716 columns]
    ```







