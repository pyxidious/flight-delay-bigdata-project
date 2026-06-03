# Preview degli output dei job

Le righe mostrate sono le prime 10 righe fisiche lette dagli output distribuiti HDFS. Poiché non viene applicato un ordinamento globale finale, l'ordine delle righe può variare tra esecuzioni o ambienti diversi. La semantica e lo schema degli output rimangono invariati.

Queste run sono state eseguite solo per produrre preview dei risultati e non fanno parte del benchmark temporale.

## 100k

### analysis_1

#### hive

```text
9E,ABE,12,-38.0,74.0,-4.0833,0,0.0,1
9E,AEX,12,-29.0,27.0,-15.0,0,0.0,1
9E,AGS,11,-35.0,7.0,-22.3636,0,0.0,1
9E,ALB,6,-43.0,-12.0,-35.0,0,0.0,1
9E,ATL,466,-33.0,193.0,-7.6009,0,0.0,1
9E,ATW,17,-33.0,167.0,6.8824,0,0.0,1
9E,AUS,5,-14.0,148.0,53.0,0,0.0,1
9E,AVL,23,-36.0,207.0,-4.6957,0,0.0,1
9E,AZO,12,-22.0,71.0,-4.6667,0,0.0,1
9E,BDL,11,-31.0,69.0,-16.0,0,0.0,1

```

#### spark_core

```text
airline,origin,total_flights,min_arr_delay,max_arr_delay,avg_arr_delay,cancelled_flights,cancellation_rate,active_months
9E,RIC,29,-42.0,67.0,-17.069,0,0.0,1
9E,JAX,18,-45.0,16.0,-21.5556,0,0.0,1
9E,LGA,244,-52.0,90.0,-22.7078,1,0.004098,1
9E,CHS,23,-34.0,9.0,-19.2174,0,0.0,1
9E,ITH,12,-37.0,42.0,-5.3333,0,0.0,1
9E,CMH,15,-31.0,344.0,14.0667,0,0.0,1
9E,ATL,466,-33.0,193.0,-7.6009,0,0.0,1
9E,STL,34,-30.0,35.0,-8.8529,0,0.0,1
9E,SAV,24,-36.0,7.0,-17.0833,0,0.0,1

```

#### spark_sql

```text
airline,origin,total_flights,min_arr_delay,max_arr_delay,avg_arr_delay,cancelled_flights,cancellation_rate,active_months
9E,ABE,12,-38.0,74.0,-4.0833,0,0.0,1
9E,AEX,12,-29.0,27.0,-15.0,0,0.0,1
9E,AGS,11,-35.0,7.0,-22.3636,0,0.0,1
9E,ALB,6,-43.0,-12.0,-35.0,0,0.0,1
9E,ATL,466,-33.0,193.0,-7.6009,0,0.0,1
9E,ATW,17,-33.0,167.0,6.8824,0,0.0,1
9E,AUS,5,-14.0,148.0,53.0,0,0.0,1
9E,AVL,23,-36.0,207.0,-4.6957,0,0.0,1
9E,AZO,12,-22.0,71.0,-4.6667,0,0.0,1

```

### analysis_2

#### hive

```text
ABE,1,high,7,268.8571,244.0,1:Delay_carrier=4; 2:Delay_late_aircraft=3
ABE,1,low,61,-4.0492,-18.7213,1:Delay_nas=3
ABE,1,medium,7,31.8571,45.0,1:Delay_nas=3; 2:Delay_carrier=2; 3:Delay_late_aircraft=2
ABI,1,low,30,-5.9,-5.3667,1:Delay_nas=3
ABQ,1,high,20,174.35,180.9,1:Delay_late_aircraft=16; 2:Delay_carrier=4
ABQ,1,low,272,-1.4191,-5.7537,1:Delay_nas=20; 2:Delay_carrier=4; 3:Delay_late_aircraft=1
ABQ,1,medium,50,29.14,25.92,1:Delay_late_aircraft=12; 2:Delay_carrier=8; 3:Delay_nas=6
ABR,1,high,2,165.0,148.0,1:Delay_carrier=1; 2:Delay_weather=1
ABR,1,low,7,-5.7143,-15.0,NoCauseAvailable
ABY,1,low,9,-2.1111,-8.7778,1:Delay_weather=1

```

#### spark_core

```text
origin,month,dep_delay_band,flight_count,avg_dep_delay,avg_arr_delay,top_3_causes
JFK,1,low,1345,-1.9792,-19.6414,1:Delay_nas=65; 2:Delay_carrier=3; 3:Cancellation_C=1
MSP,1,low,1584,-2.9457,-16.5752,1:Delay_nas=28; 2:Delay_carrier=14; 3:Delay_late_aircraft=1
DTW,1,low,1539,-2.8596,-11.7633,1:Delay_nas=86; 2:Delay_carrier=9; 3:Delay_late_aircraft=1
CLE,1,low,447,-3.8076,-12.7646,1:Delay_nas=17; 2:Delay_carrier=1; 3:Delay_late_aircraft=1
GRR,1,low,234,-5.0897,-16.2906,1:Delay_nas=7; 2:Delay_late_aircraft=2; 3:Delay_carrier=1
TLH,1,low,73,-2.7534,-3.6301,1:Delay_nas=4; 2:Delay_late_aircraft=1
CLT,1,low,2360,-1.8564,-9.0008,1:Delay_nas=81; 2:Delay_carrier=5; 3:Delay_late_aircraft=3
PVD,1,low,151,-3.894,-14.0596,1:Delay_nas=3
MIA,1,low,1466,-0.839,-3.942,1:Delay_nas=137; 2:Delay_carrier=8; 3:Delay_late_aircraft=6

```

#### spark_sql

```text
origin,month,dep_delay_band,flight_count,avg_dep_delay,avg_arr_delay,top_3_causes
BGR,1,low,37,-5.7838,-24.7568,1:Delay_nas=1
TYS,1,low,178,-5.3989,-14.0056,1:Delay_nas=7; 2:Delay_carrier=1
VLD,1,low,10,-4.2,-14.7,NoCauseAvailable
ELP,1,high,10,98.1,94.9,1:Delay_late_aircraft=8; 2:Delay_carrier=2
AMA,1,high,3,183.3333,195.3333,1:Delay_late_aircraft=2; 2:Delay_carrier=1
SMF,1,low,693,-2.5065,-7.4191,1:Delay_nas=15; 2:Delay_carrier=2
LAX,1,high,140,157.6929,151.9856,1:Delay_carrier=69; 2:Delay_late_aircraft=63; 3:Delay_nas=3
COS,1,low,144,-2.1944,-3.9514,1:Delay_nas=8
ACY,1,medium,9,25.8889,14.2222,1:Delay_nas=3; 2:Delay_carrier=1; 3:Delay_late_aircraft=1

```

### analysis_3

#### hive

```text
ABE,9E,12,11.4167,-4.0833,0,0.0,24.7733,-13.3567,1
ABE,G4,37,12.1622,3.0541,0,0.0,24.7733,-12.6112,2
ABE,OH,17,23.875,7.625,1,0.058824,24.7733,-0.8983,3
ABE,OO,10,88.9,69.5,0,0.0,24.7733,64.1267,4
ABI,MQ,30,-5.9,-5.3667,0,0.0,-5.9,0.0,1
ABQ,DL,25,-4.24,-5.96,0,0.0,13.3275,-17.5675,1
ABQ,MQ,5,3.6,0.0,0,0.0,13.3275,-9.7275,2
ABQ,AS,6,7.0,6.8333,0,0.0,13.3275,-6.3275,3
ABQ,OO,52,8.7308,4.1346,0,0.0,13.3275,-4.5967,4
ABQ,AA,52,13.8269,14.3462,0,0.0,13.3275,0.4994,5

```

#### spark_core

```text
origin,airline,total_flights,avg_dep_delay,avg_arr_delay,cancelled_flights,cancellation_rate,airport_avg_dep_delay,dep_delay_diff_from_airport,airport_rank_by_avg_dep_delay
HPN,OO,4,-4.5,-20.75,0,0.0,17.5978,-22.0978,1
HPN,OH,40,-1.475,-14.475,0,0.0,17.5978,-19.0728,2
HPN,MQ,22,5.0,-2.8182,0,0.0,17.5978,-12.5978,3
HPN,B6,82,13.4756,13.0,0,0.0,17.5978,-4.1222,4
HPN,YX,3,16.3333,-3.6667,0,0.0,17.5978,-1.2645,5
HPN,DL,24,46.2917,36.4583,0,0.0,17.5978,28.6938,6
HPN,9E,9,104.4444,88.7778,0,0.0,17.5978,86.8466,7
BQN,UA,5,-8.0,-15.2,0,0.0,6.1786,-14.1786,1
BQN,F9,17,-2.0,2.7647,0,0.0,6.1786,-8.1786,2

```

#### spark_sql

```text
origin,airline,total_flights,avg_dep_delay,avg_arr_delay,cancelled_flights,cancellation_rate,airport_avg_dep_delay,dep_delay_diff_from_airport,airport_rank_by_avg_dep_delay
ABE,9E,12,11.4167,-4.0833,0,0.0,24.7733,-13.3567,1
ABE,G4,37,12.1622,3.0541,0,0.0,24.7733,-12.6112,2
ABE,OH,17,23.875,7.625,1,0.058824,24.7733,-0.8983,3
ABE,OO,10,88.9,69.5,0,0.0,24.7733,64.1267,4
ABI,MQ,30,-5.9,-5.3667,0,0.0,-5.9,0.0,1
ABQ,DL,25,-4.24,-5.96,0,0.0,13.3275,-17.5675,1
ABQ,MQ,5,3.6,0.0,0,0.0,13.3275,-9.7275,2
ABQ,AS,6,7.0,6.8333,0,0.0,13.3275,-6.3275,3
ABQ,OO,52,8.7308,4.1346,0,0.0,13.3275,-4.5967,4

```

## 500k

### analysis_1

#### hive

```text
9E,ABE,74,-44.0,438.0,17.0685,0,0.0,1
9E,ABY,3,7.0,43.0,23.0,0,0.0,1
9E,AEX,58,-29.0,598.0,22.8929,2,0.034483,1
9E,AGS,69,-35.0,784.0,39.087,0,0.0,1
9E,ALB,93,-44.0,223.0,1.9205,5,0.053763,1
9E,ATL,2359,-36.0,951.0,16.8955,64,0.02713,1
9E,ATW,22,-34.0,167.0,9.0,0,0.0,1
9E,AUS,43,-17.0,469.0,40.381,1,0.023256,1
9E,AVL,46,-36.0,207.0,1.6957,0,0.0,1
9E,AZO,14,-22.0,71.0,-2.9286,0,0.0,1

```

#### spark_core

```text
airline,origin,total_flights,min_arr_delay,max_arr_delay,avg_arr_delay,cancelled_flights,cancellation_rate,active_months
9E,RIC,134,-42.0,1101.0,26.1077,4,0.029851,1
9E,JAX,82,-52.0,860.0,5.5,2,0.02439,1
9E,LGA,2204,-55.0,735.0,6.4647,161,0.073049,1
9E,CHS,136,-41.0,733.0,6.0469,8,0.058824,1
9E,ITH,58,-49.0,385.0,-0.7547,5,0.086207,1
9E,CMH,18,-31.0,344.0,9.0,0,0.0,1
9E,ATL,2359,-36.0,951.0,16.8955,64,0.02713,1
9E,STL,136,-32.0,305.0,4.264,10,0.073529,1
9E,SAV,159,-46.0,405.0,6.32,8,0.050314,1

```

#### spark_sql

```text
airline,origin,total_flights,min_arr_delay,max_arr_delay,avg_arr_delay,cancelled_flights,cancellation_rate,active_months
9E,ABE,74,-44.0,438.0,17.0685,0,0.0,1
9E,ABY,3,7.0,43.0,23.0,0,0.0,1
9E,AEX,58,-29.0,598.0,22.8929,2,0.034483,1
9E,AGS,69,-35.0,784.0,39.087,0,0.0,1
9E,ALB,93,-44.0,223.0,1.9205,5,0.053763,1
9E,ATL,2359,-36.0,951.0,16.8955,64,0.02713,1
9E,ATW,22,-34.0,167.0,9.0,0,0.0,1
9E,AUS,43,-17.0,469.0,40.381,1,0.023256,1
9E,AVL,46,-36.0,207.0,1.6957,0,0.0,1

```

### analysis_2

#### hive

```text
ABE,1,high,30,241.3,234.0333,1:Delay_late_aircraft=14; 2:Delay_carrier=12; 3:Delay_nas=2
ABE,1,low,251,-5.2948,-13.0241,1:Delay_nas=20; 2:Delay_carrier=1
ABE,1,medium,30,33.6,32.7586,1:Delay_late_aircraft=12; 2:Delay_carrier=7; 3:Delay_nas=3
ABI,1,high,14,112.5,123.8462,1:Delay_late_aircraft=9; 2:Delay_weather=3; 3:Cancellation_B=1
ABI,1,low,111,-6.009,-3.3153,1:Delay_nas=10
ABI,1,medium,11,38.9091,36.7273,1:Delay_late_aircraft=7; 2:Delay_weather=2; 3:Delay_carrier=1
ABQ,1,high,108,139.0648,136.3241,1:Delay_late_aircraft=74; 2:Delay_carrier=20; 3:Delay_nas=7
ABQ,1,low,1312,-2.9688,-7.7435,1:Delay_nas=56; 2:Delay_carrier=12; 3:Delay_late_aircraft=2
ABQ,1,medium,198,30.9949,26.4394,1:Delay_late_aircraft=85; 2:Delay_carrier=33; 3:Delay_nas=16
ABR,1,high,5,130.8,121.4,1:Delay_carrier=3; 2:Delay_weather=2

```

#### spark_core

```text
origin,month,dep_delay_band,flight_count,avg_dep_delay,avg_arr_delay,top_3_causes
JFK,1,low,6537,-2.5685,-12.1029,1:Delay_nas=577; 2:Delay_carrier=35; 3:Delay_late_aircraft=3
MSP,1,low,6769,-2.3311,-11.3877,1:Delay_nas=378; 2:Delay_carrier=106; 3:Delay_late_aircraft=6
DTW,1,low,6038,-1.8501,-6.1489,1:Delay_nas=687; 2:Delay_carrier=80; 3:Cancellation_B=9
CLE,1,low,2029,-3.8004,-8.8123,1:Delay_nas=152; 2:Delay_carrier=8; 3:Cancellation_A=1
GRR,1,low,979,-3.9275,-6.5961,1:Delay_nas=136; 2:Delay_carrier=8; 3:Delay_late_aircraft=6
TLH,1,low,352,-3.7869,-6.1425,1:Delay_nas=16; 2:Delay_late_aircraft=3
CLT,1,low,10717,-1.7701,-6.339,1:Delay_nas=611; 2:Delay_carrier=47; 3:Delay_late_aircraft=29
PVD,1,low,638,-3.2461,-8.7767,1:Delay_nas=38; 2:Delay_late_aircraft=5; 3:Delay_carrier=3
MIA,1,low,6319,-0.8118,-5.3909,1:Delay_nas=552; 2:Delay_carrier=43; 3:Delay_late_aircraft=19

```

#### spark_sql

```text
origin,month,dep_delay_band,flight_count,avg_dep_delay,avg_arr_delay,top_3_causes
BGR,1,low,166,-7.4096,-17.7289,1:Delay_nas=9; 2:Delay_carrier=1
TYS,1,low,743,-5.3378,-10.1226,1:Delay_nas=64; 2:Delay_carrier=4
VLD,1,low,50,-5.28,-13.0,NoCauseAvailable
ELP,1,high,64,164.6719,164.8906,1:Delay_late_aircraft=38; 2:Delay_carrier=14; 3:Delay_weather=8
AMA,1,high,30,173.9,168.5333,1:Delay_late_aircraft=19; 2:Delay_carrier=6; 3:Delay_weather=3
SMF,1,low,3058,-2.4621,-8.2282,1:Delay_nas=72; 2:Delay_carrier=28; 3:Delay_late_aircraft=3
LAX,1,high,791,154.0063,147.1874,1:Delay_late_aircraft=378; 2:Delay_carrier=303; 3:Delay_nas=58
COS,1,low,692,-3.0636,-6.0377,1:Delay_nas=43; 2:Delay_carrier=6; 3:Cancellation_A=1
ACY,1,medium,23,29.9565,31.6087,1:Delay_nas=9; 2:Delay_late_aircraft=5; 3:Delay_carrier=3

```

### analysis_3

#### hive

```text
ABE,9E,74,20.8514,17.0685,0,0.0,22.2444,-1.393,1
ABE,G4,129,21.4264,14.7364,0,0.0,22.2444,-0.818,2
ABE,OH,83,22.0759,14.4103,4,0.048193,22.2444,-0.1684,3
ABE,OO,36,29.8966,16.3214,7,0.194444,22.2444,7.6522,4
ABI,MQ,137,9.8235,12.1926,2,0.014599,9.8235,0.0,1
ABQ,DL,100,0.2,-5.0404,0,0.0,10.6681,-10.4681,1
ABQ,OO,298,5.9428,0.1886,1,0.003356,10.6681,-4.7253,2
ABQ,UA,117,6.693,2.6195,4,0.034188,10.6681,-3.9751,3
ABQ,MQ,44,7.4048,4.6905,2,0.045455,10.6681,-3.2633,4
ABQ,WN,814,10.8593,5.2399,18,0.022113,10.6681,0.1912,5

```

#### spark_core

```text
origin,airline,total_flights,avg_dep_delay,avg_arr_delay,cancelled_flights,cancellation_rate,airport_avg_dep_delay,dep_delay_diff_from_airport,airport_rank_by_avg_dep_delay
HPN,B6,397,10.9211,16.6308,4,0.010076,24.7885,-13.8674,1
HPN,YX,5,18.8,2.2,0,0.0,24.7885,-5.9885,2
HPN,OH,198,25.9617,20.5191,15,0.075758,24.7885,1.1732,3
HPN,MQ,106,30.7653,27.898,8,0.075472,24.7885,5.9768,4
HPN,DL,112,36.75,34.4054,0,0.0,24.7885,11.9615,5
HPN,9E,72,37.9155,29.0282,1,0.013889,24.7885,13.127,6
HPN,OO,87,55.2658,45.8861,8,0.091954,24.7885,30.4773,7
BQN,B6,132,2.7328,-0.8855,1,0.007576,9.4292,-6.6964,1
BQN,F9,53,9.6415,9.3585,0,0.0,9.4292,0.2123,2

```

#### spark_sql

```text
origin,airline,total_flights,avg_dep_delay,avg_arr_delay,cancelled_flights,cancellation_rate,airport_avg_dep_delay,dep_delay_diff_from_airport,airport_rank_by_avg_dep_delay
ABE,9E,74,20.8514,17.0685,0,0.0,22.2444,-1.393,1
ABE,G4,129,21.4264,14.7364,0,0.0,22.2444,-0.818,2
ABE,OH,83,22.0759,14.4103,4,0.048193,22.2444,-0.1684,3
ABE,OO,36,29.8966,16.3214,7,0.194444,22.2444,7.6522,4
ABI,MQ,137,9.8235,12.1926,2,0.014599,9.8235,0.0,1
ABQ,DL,100,0.2,-5.0404,0,0.0,10.6681,-10.4681,1
ABQ,OO,298,5.9428,0.1886,1,0.003356,10.6681,-4.7253,2
ABQ,UA,117,6.693,2.6195,4,0.034188,10.6681,-3.9751,3
ABQ,MQ,44,7.4048,4.6905,2,0.045455,10.6681,-3.2633,4

```

## 1m

### analysis_1

#### hive

```text
9E,ABE,147,-44.0,438.0,2.8276,1,0.006803,1,2
9E,ABY,7,-15.0,321.0,54.7143,0,0.0,1,2
9E,AEX,114,-34.0,598.0,8.9107,2,0.017544,1,2
9E,AGS,145,-36.0,784.0,16.4483,0,0.0,1,2
9E,ALB,180,-51.0,223.0,-7.7688,7,0.038889,1,2
9E,ATL,4291,-43.0,953.0,6.9187,66,0.015381,1,2
9E,ATW,22,-34.0,167.0,9.0,0,0.0,1
9E,AUS,95,-28.0,469.0,17.7447,1,0.010526,1,2
9E,AVL,74,-36.0,207.0,-3.5135,0,0.0,1,2
9E,AZO,14,-22.0,71.0,-2.9286,0,0.0,1

```

#### spark_core

```text
airline,origin,total_flights,min_arr_delay,max_arr_delay,avg_arr_delay,cancelled_flights,cancellation_rate,active_months
9E,RIC,278,-42.0,1101.0,11.6052,7,0.02518,"1,2"
9E,JAX,160,-52.0,860.0,-0.7821,4,0.025,"1,2"
9E,LGA,4802,-62.0,735.0,-6.0396,226,0.047064,"1,2"
9E,CHS,276,-41.0,733.0,-0.6805,10,0.036232,"1,2"
9E,ITH,114,-52.0,385.0,-12.1759,6,0.052632,"1,2"
9E,CMH,18,-31.0,344.0,9.0,0,0.0,1
9E,ATL,4291,-43.0,953.0,6.9187,66,0.015381,"1,2"
9E,STL,260,-35.0,305.0,-2.2632,12,0.046154,"1,2"
9E,SAV,323,-46.0,405.0,2.5858,11,0.034056,"1,2"

```

#### spark_sql

```text
airline,origin,total_flights,min_arr_delay,max_arr_delay,avg_arr_delay,cancelled_flights,cancellation_rate,active_months
9E,ABE,147,-44.0,438.0,2.8276,1,0.006803,"1,2"
9E,ABY,7,-15.0,321.0,54.7143,0,0.0,"1,2"
9E,AEX,114,-34.0,598.0,8.9107,2,0.017544,"1,2"
9E,AGS,145,-36.0,784.0,16.4483,0,0.0,"1,2"
9E,ALB,180,-51.0,223.0,-7.7688,7,0.038889,"1,2"
9E,ATL,4291,-43.0,953.0,6.9187,66,0.015381,"1,2"
9E,ATW,22,-34.0,167.0,9.0,0,0.0,1
9E,AUS,95,-28.0,469.0,17.7447,1,0.010526,"1,2"
9E,AVL,74,-36.0,207.0,-3.5135,0,0.0,"1,2"

```

### analysis_2

#### hive

```text
ABE,1,high,30,241.3,234.0333,1:Delay_late_aircraft=14; 2:Delay_carrier=12; 3:Delay_nas=2
ABE,1,low,277,-5.509,-14.5564,1:Delay_nas=20; 2:Delay_carrier=1
ABE,1,medium,31,34.3226,32.5,1:Delay_late_aircraft=12; 2:Delay_carrier=8; 3:Delay_nas=3
ABE,2,high,13,237.3077,227.7692,1:Delay_carrier=6; 2:Delay_late_aircraft=5; 3:Delay_nas=1
ABE,2,low,255,-6.7725,-19.6417,1:Delay_nas=10; 2:Delay_carrier=1; 3:Delay_weather=1
ABE,2,medium,18,28.5,10.3333,1:Delay_carrier=5; 2:Delay_late_aircraft=3
ABI,1,high,14,112.5,123.8462,1:Delay_late_aircraft=9; 2:Delay_weather=3; 3:Cancellation_B=1
ABI,1,low,125,-6.344,-4.056,1:Delay_nas=10
ABI,1,medium,11,38.9091,36.7273,1:Delay_late_aircraft=7; 2:Delay_weather=2; 3:Delay_carrier=1
ABI,2,high,1,99.0,88.0,1:Delay_weather=1

```

#### spark_core

```text
origin,month,dep_delay_band,flight_count,avg_dep_delay,avg_arr_delay,top_3_causes
JFK,1,low,7233,-2.817,-14.054,1:Delay_nas=584; 2:Delay_carrier=36; 3:Delay_late_aircraft=3
MSP,1,low,7554,-2.5821,-12.5667,1:Delay_nas=384; 2:Delay_carrier=108; 3:Delay_late_aircraft=6
DTW,1,low,6780,-2.0569,-7.1532,1:Delay_nas=720; 2:Delay_carrier=86; 3:Cancellation_B=9
CLE,1,low,2278,-4.0097,-10.0902,1:Delay_nas=160; 2:Delay_carrier=9; 3:Cancellation_A=1
GRR,1,low,1098,-4.2177,-8.515,1:Delay_nas=137; 2:Delay_carrier=8; 3:Delay_late_aircraft=6
TLH,1,low,390,-3.9256,-6.2699,1:Delay_nas=19; 2:Delay_late_aircraft=3
CLT,1,low,11805,-1.9366,-6.7901,1:Delay_nas=637; 2:Delay_carrier=49; 3:Delay_late_aircraft=29
PVD,1,low,714,-3.4524,-10.0098,1:Delay_nas=38; 2:Delay_late_aircraft=6; 3:Delay_carrier=3
MIA,1,low,6893,-0.9502,-5.2774,1:Delay_nas=602; 2:Delay_carrier=47; 3:Delay_late_aircraft=20

```

#### spark_sql

```text
origin,month,dep_delay_band,flight_count,avg_dep_delay,avg_arr_delay,top_3_causes
BGR,1,low,182,-7.4505,-18.8901,1:Delay_nas=9; 2:Delay_carrier=1
TYS,1,low,820,-5.5744,-10.3187,1:Delay_nas=73; 2:Delay_carrier=4
VLD,1,low,54,-5.3519,-13.1111,NoCauseAvailable
ELP,1,high,64,164.6719,164.8906,1:Delay_late_aircraft=38; 2:Delay_carrier=14; 3:Delay_weather=8
AMA,1,high,30,173.9,168.5333,1:Delay_late_aircraft=19; 2:Delay_carrier=6; 3:Delay_weather=3
SMF,1,low,3409,-2.6709,-8.3452,1:Delay_nas=78; 2:Delay_carrier=31; 3:Delay_late_aircraft=3
LAX,1,high,828,154.3514,147.8027,1:Delay_late_aircraft=388; 2:Delay_carrier=328; 3:Delay_nas=60
COS,1,low,774,-3.3953,-6.5953,1:Delay_nas=46; 2:Delay_carrier=6; 3:Cancellation_A=1
ACY,1,medium,24,29.375,30.875,1:Delay_nas=9; 2:Delay_late_aircraft=5; 3:Delay_carrier=3

```

### analysis_3

#### hive

```text
ABE,OH,167,9.9691,-1.6894,5,0.02994,13.859,-3.8898,1
ABE,OO,71,11.0952,-1.0161,8,0.112676,13.859,-2.7637,2
ABE,9E,147,13.0411,2.8276,1,0.006803,13.859,-0.8179,3
ABE,G4,253,17.5099,8.2381,0,0.0,13.859,3.6509,4
ABI,MQ,273,2.6581,3.7269,2,0.007326,2.6581,0.0,1
ABQ,DL,194,-1.9278,-9.0415,0,0.0,8.557,-10.4848,1
ABQ,OO,601,5.6466,1.2919,4,0.006656,8.557,-2.9104,2
ABQ,MQ,65,6.381,3.1111,2,0.030769,8.557,-2.176,3
ABQ,UA,217,8.0093,2.5802,5,0.023041,8.557,-0.5476,4
ABQ,NK,36,8.75,0.5278,0,0.0,8.557,0.193,5

```

#### spark_core

```text
origin,airline,total_flights,avg_dep_delay,avg_arr_delay,cancelled_flights,cancellation_rate,airport_avg_dep_delay,dep_delay_diff_from_airport,airport_rank_by_avg_dep_delay
HPN,B6,796,9.0901,7.4459,8,0.01005,16.0797,-6.9896,1
HPN,OH,396,17.0794,8.4894,18,0.045455,16.0797,0.9997,2
HPN,MQ,213,18.7438,11.5123,10,0.046948,16.0797,2.6642,3
HPN,YX,5,18.8,2.2,0,0.0,16.0797,2.7203,4
HPN,9E,164,19.858,7.2531,2,0.012195,16.0797,3.7783,5
HPN,DL,227,24.2291,14.4027,0,0.0,16.0797,8.1494,6
HPN,OO,166,29.5414,17.0127,9,0.054217,16.0797,13.4617,7
BQN,F9,89,8.4545,9.9773,1,0.011236,10.0627,-1.6081,1
BQN,B6,259,9.1176,6.8898,4,0.015444,10.0627,-0.945,2

```

#### spark_sql

```text
origin,airline,total_flights,avg_dep_delay,avg_arr_delay,cancelled_flights,cancellation_rate,airport_avg_dep_delay,dep_delay_diff_from_airport,airport_rank_by_avg_dep_delay
ABE,OH,167,9.9691,-1.6894,5,0.02994,13.859,-3.8898,1
ABE,OO,71,11.0952,-1.0161,8,0.112676,13.859,-2.7637,2
ABE,9E,147,13.0411,2.8276,1,0.006803,13.859,-0.8179,3
ABE,G4,253,17.5099,8.2381,0,0.0,13.859,3.6509,4
ABI,MQ,273,2.6581,3.7269,2,0.007326,2.6581,0.0,1
ABQ,DL,194,-1.9278,-9.0415,0,0.0,8.557,-10.4848,1
ABQ,OO,601,5.6466,1.2919,4,0.006656,8.557,-2.9104,2
ABQ,MQ,65,6.381,3.1111,2,0.030769,8.557,-2.176,3
ABQ,UA,217,8.0093,2.5802,5,0.023041,8.557,-0.5476,4

```

## 3m

### analysis_1

#### hive

```text
9E,ABE,441,-47.0,438.0,-1.2808,2,0.004535,1,2,3,4,5,6
9E,ABY,8,-15.0,321.0,48.125,0,0.0,1,2,3
9E,AEX,321,-34.0,598.0,5.6364,2,0.006231,1,2,3,4,5,6
9E,AGS,629,-36.0,784.0,6.6911,0,0.0,1,2,3,4,5,6
9E,ATW,141,-34.0,420.0,6.5,0,0.0,1,4,5,6
9E,BMI,320,-38.0,318.0,3.381,4,0.0125,1,2,3,4,5,6
9E,BNA,622,-43.0,1132.0,14.7842,13,0.0209,1,2,3,4,5,6
9E,BQK,61,-31.0,165.0,1.6557,0,0.0,3,4,6
9E,BTR,249,-34.0,1006.0,5.4609,4,0.016064,1,2,3,5,6
9E,BTV,762,-48.0,752.0,-0.0524,17,0.02231,1,2,3,4,5,6

```

#### spark_core

```text
airline,origin,total_flights,min_arr_delay,max_arr_delay,avg_arr_delay,cancelled_flights,cancellation_rate,active_months
9E,JAX,437,-52.0,860.0,-1.6192,8,0.018307,"1,2,3,4,5,6"
9E,IND,1127,-44.0,847.0,-3.2905,19,0.016859,"1,2,3,4,5,6"
9E,PHL,105,-36.0,173.0,-1.9905,0,0.0,"1,2,3"
9E,PNS,176,-42.0,1089.0,17.3161,2,0.011364,"1,2,3,4,5,6"
9E,FAY,119,-32.0,264.0,0.0168,0,0.0,"1,2,3,4,5,6"
9E,ROC,1159,-49.0,816.0,0.4707,28,0.024159,"1,2,3,4,5,6"
9E,AEX,321,-34.0,598.0,5.6364,2,0.006231,"1,2,3,4,5,6"
9E,OAJ,166,-34.0,1157.0,4.3133,0,0.0,"1,2,3,4,5,6"
9E,ICT,118,-34.0,90.0,1.4831,0,0.0,"1,2,3"

```

#### spark_sql

```text
airline,origin,total_flights,min_arr_delay,max_arr_delay,avg_arr_delay,cancelled_flights,cancellation_rate,active_months
9E,ABE,441,-47.0,438.0,-1.2808,2,0.004535,"1,2,3,4,5,6"
9E,ABY,8,-15.0,321.0,48.125,0,0.0,"1,2,3"
9E,AEX,321,-34.0,598.0,5.6364,2,0.006231,"1,2,3,4,5,6"
9E,AGS,629,-36.0,784.0,6.6911,0,0.0,"1,2,3,4,5,6"
9E,ALB,560,-51.0,380.0,-6.2468,8,0.014286,"1,2,3,4,5,6"
9E,ATL,10899,-43.0,1207.0,2.7117,75,0.006881,"1,2,3,4,5,6"
9E,ATW,141,-34.0,420.0,6.5,0,0.0,"1,4,5,6"
9E,AUS,327,-35.0,1225.0,14.681,1,0.003058,"1,2,3,4,5,6"
9E,AVL,229,-37.0,835.0,6.4493,0,0.0,"1,2,3,4,5,6"

```

### analysis_2

#### hive

```text
ABE,1,high,30,241.3,234.0333,1:Delay_late_aircraft=14; 2:Delay_carrier=12; 3:Delay_nas=2
ABE,1,low,277,-5.509,-14.5564,1:Delay_nas=20; 2:Delay_carrier=1
ABE,1,medium,31,34.3226,32.5,1:Delay_late_aircraft=12; 2:Delay_carrier=8; 3:Delay_nas=3
ABE,2,high,14,227.9286,217.9286,1:Delay_carrier=6; 2:Delay_late_aircraft=6; 3:Delay_nas=1
ABE,2,low,297,-6.6498,-19.5709,1:Delay_nas=10; 2:Delay_carrier=1; 3:Delay_weather=1
ABE,2,medium,20,29.7,10.1053,1:Delay_carrier=5; 2:Delay_late_aircraft=3
ABE,3,high,23,173.4348,163.3913,1:Delay_carrier=9; 2:Delay_late_aircraft=8; 3:Delay_nas=6
ABE,3,low,339,-6.1858,-18.3687,1:Delay_nas=7
ABE,3,medium,28,30.6786,19.8929,1:Delay_late_aircraft=7; 2:Delay_carrier=4; 3:Delay_nas=4
ABE,4,high,29,258.6552,250.3793,1:Delay_carrier=16; 2:Delay_late_aircraft=7; 3:Delay_nas=4

```

#### spark_core

```text
origin,month,dep_delay_band,flight_count,avg_dep_delay,avg_arr_delay,top_3_causes
MSP,1,low,7554,-2.5821,-12.5667,1:Delay_nas=384; 2:Delay_carrier=108; 3:Delay_late_aircraft=6
DTW,1,low,6780,-2.0569,-7.1532,1:Delay_nas=720; 2:Delay_carrier=86; 3:Cancellation_B=9
CLE,1,low,2278,-4.0097,-10.0902,1:Delay_nas=160; 2:Delay_carrier=9; 3:Cancellation_A=1
TLH,1,low,390,-3.9256,-6.2699,1:Delay_nas=19; 2:Delay_late_aircraft=3
PVD,1,low,714,-3.4524,-10.0098,1:Delay_nas=38; 2:Delay_late_aircraft=6; 3:Delay_carrier=3
MIA,1,low,6893,-0.9502,-5.2774,1:Delay_nas=602; 2:Delay_carrier=47; 3:Delay_late_aircraft=20
EYW,1,low,586,-4.3618,-9.4966,1:Delay_nas=24; 2:Delay_carrier=4; 3:Delay_late_aircraft=1
TYS,1,low,820,-5.5744,-10.3187,1:Delay_nas=73; 2:Delay_carrier=4
CLT,1,high,1657,136.478,132.7814,1:Delay_late_aircraft=1046; 2:Delay_carrier=425; 3:Delay_weather=135

```

#### spark_sql

```text
origin,month,dep_delay_band,flight_count,avg_dep_delay,avg_arr_delay,top_3_causes
BGR,1,low,182,-7.4505,-18.8901,1:Delay_nas=9; 2:Delay_carrier=1
TYS,1,low,820,-5.5744,-10.3187,1:Delay_nas=73; 2:Delay_carrier=4
VLD,1,low,54,-5.3519,-13.1111,NoCauseAvailable
ELP,1,high,64,164.6719,164.8906,1:Delay_late_aircraft=38; 2:Delay_carrier=14; 3:Delay_weather=8
AMA,1,high,30,173.9,168.5333,1:Delay_late_aircraft=19; 2:Delay_carrier=6; 3:Delay_weather=3
SMF,1,low,3409,-2.6709,-8.3452,1:Delay_nas=78; 2:Delay_carrier=31; 3:Delay_late_aircraft=3
LAX,1,high,828,154.3514,147.8027,1:Delay_late_aircraft=388; 2:Delay_carrier=328; 3:Delay_nas=60
COS,1,low,774,-3.3953,-6.5953,1:Delay_nas=46; 2:Delay_carrier=6; 3:Cancellation_A=1
ACY,1,medium,24,29.375,30.875,1:Delay_nas=9; 2:Delay_late_aircraft=5; 3:Delay_carrier=3

```

### analysis_3

#### hive

```text
ABE,9E,441,9.4556,-1.2808,2,0.004535,13.1205,-3.665,1
ABE,G4,740,10.768,1.7337,3,0.004054,13.1205,-2.3526,2
ABE,OH,476,11.258,1.3483,7,0.014706,13.1205,-1.8625,3
ABE,OO,274,29.1521,19.3166,11,0.040146,13.1205,16.0315,4
ABI,MQ,765,12.0424,10.5551,12,0.015686,12.0424,0.0,1
ABQ,DL,593,0.8162,-6.8071,0,0.0,11.439,-10.6228,1
ABQ,OO,1724,4.8126,0.8669,16,0.009281,11.439,-6.6264,2
ABQ,NK,201,7.6985,-0.5879,2,0.00995,11.439,-3.7405,3
ABQ,MQ,205,9.065,7.2764,5,0.02439,11.439,-2.374,4
ABQ,UA,699,9.3862,3.391,7,0.010014,11.439,-2.0529,5

```

#### spark_core

```text
origin,airline,total_flights,avg_dep_delay,avg_arr_delay,cancelled_flights,cancellation_rate,airport_avg_dep_delay,dep_delay_diff_from_airport,airport_rank_by_avg_dep_delay
HPN,YX,59,7.4746,1.0508,0,0.0,12.6879,-5.2134,1
HPN,B6,2238,8.6831,2.9654,25,0.011171,12.6879,-4.0049,2
HPN,MQ,578,9.2842,2.27,15,0.025952,12.6879,-3.4037,3
HPN,9E,437,13.552,2.3718,4,0.009153,12.6879,0.864,4
HPN,OH,1162,14.4583,10.1048,23,0.019793,12.6879,1.7704,5
HPN,DL,569,18.0159,7.2695,3,0.005272,12.6879,5.328,6
HPN,OO,458,25.4139,15.1734,11,0.024017,12.6879,12.7259,7
BQN,F9,272,11.2185,3.4222,2,0.007353,12.0264,-0.8079,1
BQN,B6,794,12.1327,8.6215,10,0.012594,12.0264,0.1062,2

```

#### spark_sql

```text
origin,airline,total_flights,avg_dep_delay,avg_arr_delay,cancelled_flights,cancellation_rate,airport_avg_dep_delay,dep_delay_diff_from_airport,airport_rank_by_avg_dep_delay
ABE,9E,441,9.4556,-1.2808,2,0.004535,13.1205,-3.665,1
ABE,G4,740,10.768,1.7337,3,0.004054,13.1205,-2.3526,2
ABE,OH,476,11.258,1.3483,7,0.014706,13.1205,-1.8625,3
ABE,OO,274,29.1521,19.3166,11,0.040146,13.1205,16.0315,4
ABI,MQ,765,12.0424,10.5551,12,0.015686,12.0424,0.0,1
ABQ,DL,593,0.8162,-6.8071,0,0.0,11.439,-10.6228,1
ABQ,OO,1724,4.8126,0.8669,16,0.009281,11.439,-6.6264,2
ABQ,NK,201,7.6985,-0.5879,2,0.00995,11.439,-3.7405,3
ABQ,MQ,205,9.065,7.2764,5,0.02439,11.439,-2.374,4

```

## 7m

### analysis_1

#### hive

```text
9E,ATW,176,-34.0,420.0,9.3943,0,0.0,1,10,4,5,6,7,8,9
9E,BTR,502,-34.0,1015.0,5.5531,9,0.017928,1,10,11,12,2,3,5,6,7,8,9
9E,BUF,1924,-49.0,996.0,0.6033,58,0.030146,1,10,11,12,2,3,4,5,6,7,8,9
9E,CHS,1988,-46.0,849.0,3.7952,85,0.042757,1,10,11,12,2,3,4,5,6,7,8,9
9E,CID,160,-35.0,129.0,-2.6188,0,0.0,1,10,11,4,5,9
9E,CLE,2484,-48.0,1132.0,5.6678,69,0.027778,1,10,11,12,2,3,4,5,6,7,8,9
9E,CMH,252,-40.0,344.0,1.484,1,0.003968,1,10,11,12,3,4,5,6,8,9
9E,DFW,2,127.0,133.0,130.0,0,0.0,12
9E,DHN,536,-41.0,937.0,3.5677,3,0.005597,1,10,11,12,2,3,4,5,6,9
9E,EYW,159,-27.0,561.0,21.9551,3,0.018868,1,12,2,3,4,5

```

#### spark_core

```text
airline,origin,total_flights,min_arr_delay,max_arr_delay,avg_arr_delay,cancelled_flights,cancellation_rate,active_months
9E,JAX,909,-52.0,1147.0,-0.1984,25,0.027503,"1,2,3,4,5,6,7,8,9,10,11,12"
9E,IND,2416,-48.0,1086.0,-1.0803,55,0.022765,"1,2,3,4,5,6,7,8,9,10,11,12"
9E,PHL,150,-37.0,371.0,-2.3,0,0.0,"1,2,3,11,12"
9E,PNS,265,-43.0,1089.0,16.908,3,0.011321,"1,2,3,4,5,6,7,8,9,11,12"
9E,FAY,349,-32.0,949.0,8.3696,0,0.0,"1,2,3,4,5,6,9,10,11,12"
9E,ROC,2686,-49.0,1184.0,1.3745,90,0.033507,"1,2,3,4,5,6,7,8,9,10,11,12"
9E,OAJ,548,-39.0,1157.0,0.5657,0,0.0,"1,2,3,4,5,6,7,8,9,10,11,12"
9E,ICT,168,-34.0,204.0,1.9345,0,0.0,"1,2,3,11,12"
9E,CWA,731,-44.0,386.0,-2.9034,6,0.008208,"1,2,3,4,5,6,7,8,9,10,11,12"

```

#### spark_sql

```text
airline,origin,total_flights,min_arr_delay,max_arr_delay,avg_arr_delay,cancelled_flights,cancellation_rate,active_months
9E,ABE,1017,-47.0,575.0,0.6693,14,0.013766,"1,10,11,12,2,3,4,5,6,7,8,9"
9E,ABY,38,-32.0,321.0,4.3684,0,0.0,"1,11,12,2,3"
9E,AEX,878,-34.0,979.0,9.6129,9,0.010251,"1,10,11,12,2,3,4,5,6,7,8,9"
9E,AGS,1603,-36.0,1091.0,6.9669,33,0.020586,"1,10,11,12,2,3,4,5,6,7,8,9"
9E,ALB,1089,-51.0,394.0,-4.3889,21,0.019284,"1,10,11,12,2,3,4,5,6,7,8,9"
9E,ATL,26877,-43.0,1207.0,2.4584,293,0.010902,"1,10,11,12,2,3,4,5,6,7,8,9"
9E,ATW,176,-34.0,420.0,9.3943,0,0.0,"1,10,4,5,6,7,8,9"
9E,AUS,379,-35.0,1225.0,14.1459,2,0.005277,"1,11,2,3,4,5,6,7"
9E,AVL,675,-43.0,949.0,1.9164,14,0.020741,"1,10,11,12,2,3,4,5,6,7,8,9"

```

### analysis_2

#### hive

```text
ABE,1,high,30,241.3,234.0333,1:Delay_late_aircraft=14; 2:Delay_carrier=12; 3:Delay_nas=2
ABE,1,low,277,-5.509,-14.5564,1:Delay_nas=20; 2:Delay_carrier=1
ABE,1,medium,31,34.3226,32.5,1:Delay_late_aircraft=12; 2:Delay_carrier=8; 3:Delay_nas=3
ABE,2,high,14,227.9286,217.9286,1:Delay_carrier=6; 2:Delay_late_aircraft=6; 3:Delay_nas=1
ABE,2,low,297,-6.6498,-19.5709,1:Delay_nas=10; 2:Delay_carrier=1; 3:Delay_weather=1
ABE,2,medium,20,29.7,10.1053,1:Delay_carrier=5; 2:Delay_late_aircraft=3
ABE,3,high,23,173.4348,163.3913,1:Delay_carrier=9; 2:Delay_late_aircraft=8; 3:Delay_nas=6
ABE,3,low,339,-6.1858,-18.3687,1:Delay_nas=7
ABE,3,medium,28,30.6786,19.8929,1:Delay_late_aircraft=7; 2:Delay_carrier=4; 3:Delay_nas=4
ABE,4,high,29,258.6552,250.3793,1:Delay_carrier=16; 2:Delay_late_aircraft=7; 3:Delay_nas=4

```

#### spark_core

```text
origin,month,dep_delay_band,flight_count,avg_dep_delay,avg_arr_delay,top_3_causes
MSP,1,low,7554,-2.5821,-12.5667,1:Delay_nas=384; 2:Delay_carrier=108; 3:Delay_late_aircraft=6
PVD,1,low,714,-3.4524,-10.0098,1:Delay_nas=38; 2:Delay_late_aircraft=6; 3:Delay_carrier=3
MIA,1,low,6893,-0.9502,-5.2774,1:Delay_nas=602; 2:Delay_carrier=47; 3:Delay_late_aircraft=20
TYS,1,low,820,-5.5744,-10.3187,1:Delay_nas=73; 2:Delay_carrier=4
CLT,1,high,1657,136.478,132.7814,1:Delay_late_aircraft=1046; 2:Delay_carrier=425; 3:Delay_weather=135
TUL,1,low,980,-3.7684,-5.8764,1:Delay_nas=77; 2:Delay_carrier=18; 3:Delay_late_aircraft=6
RST,1,low,73,-4.6712,-17.0137,NoCauseAvailable
LEX,1,low,486,-5.1852,-10.2778,1:Delay_nas=41; 2:Delay_carrier=3; 3:Delay_late_aircraft=3
LGA,1,medium,1454,32.6651,27.3873,1:Delay_late_aircraft=422; 2:Delay_carrier=349; 3:Delay_nas=146

```

#### spark_sql

```text
origin,month,dep_delay_band,flight_count,avg_dep_delay,avg_arr_delay,top_3_causes
BGR,1,low,182,-7.4505,-18.8901,1:Delay_nas=9; 2:Delay_carrier=1
TYS,1,low,820,-5.5744,-10.3187,1:Delay_nas=73; 2:Delay_carrier=4
VLD,1,low,54,-5.3519,-13.1111,NoCauseAvailable
ELP,1,high,64,164.6719,164.8906,1:Delay_late_aircraft=38; 2:Delay_carrier=14; 3:Delay_weather=8
AMA,1,high,30,173.9,168.5333,1:Delay_late_aircraft=19; 2:Delay_carrier=6; 3:Delay_weather=3
SMF,1,low,3409,-2.6709,-8.3452,1:Delay_nas=78; 2:Delay_carrier=31; 3:Delay_late_aircraft=3
LAX,1,high,828,154.3514,147.8027,1:Delay_late_aircraft=388; 2:Delay_carrier=328; 3:Delay_nas=60
COS,1,low,774,-3.3953,-6.5953,1:Delay_nas=46; 2:Delay_carrier=6; 3:Cancellation_A=1
ACY,1,medium,24,29.375,30.875,1:Delay_nas=9; 2:Delay_late_aircraft=5; 3:Delay_carrier=3

```

### analysis_3

#### hive

```text
ABE,G4,1839,8.4312,0.6431,30,0.016313,12.1596,-3.7285,1
ABE,9E,1017,9.4177,0.6693,14,0.013766,12.1596,-2.7419,2
ABE,OH,1166,15.5465,4.446,15,0.012864,12.1596,3.3868,3
ABE,OO,315,30.6304,22.3077,12,0.038095,12.1596,18.4707,4
ABI,MQ,1757,7.3098,4.4095,15,0.008537,7.3098,0.0,1
ABQ,DL,1547,1.7462,-5.6026,14,0.00905,9.4674,-7.7211,1
ABQ,OO,3987,2.1028,-2.0512,18,0.004515,9.4674,-7.3646,2
ABQ,MQ,907,5.2841,3.2584,6,0.006615,9.4674,-4.1833,3
ABQ,UA,1822,5.4881,-0.3209,19,0.010428,9.4674,-3.9793,4
ABQ,AS,423,8.4024,4.5263,4,0.009456,9.4674,-1.065,5

```

#### spark_core

```text
origin,airline,total_flights,avg_dep_delay,avg_arr_delay,cancelled_flights,cancellation_rate,airport_avg_dep_delay,dep_delay_diff_from_airport,airport_rank_by_avg_dep_delay
DTW,YX,4834,3.0815,-1.5331,78,0.016136,11.2349,-8.1534,1
DTW,9E,12740,4.8032,0.183,118,0.009262,11.2349,-6.4317,2
DTW,MQ,854,7.1867,4.7567,24,0.028103,11.2349,-4.0481,3
DTW,UA,2295,7.1951,1.8144,25,0.010893,11.2349,-4.0398,4
DTW,WN,4073,9.1507,1.9611,27,0.006629,11.2349,-2.0841,5
DTW,NK,10566,9.8168,0.8481,148,0.014007,11.2349,-1.4181,6
DTW,AS,510,9.994,4.7535,10,0.019608,11.2349,-1.2409,7
DTW,DL,58870,11.239,5.0932,519,0.008816,11.2349,0.0041,8
DTW,OH,1182,11.4129,7.5337,23,0.019459,11.2349,0.1781,9

```

#### spark_sql

```text
origin,airline,total_flights,avg_dep_delay,avg_arr_delay,cancelled_flights,cancellation_rate,airport_avg_dep_delay,dep_delay_diff_from_airport,airport_rank_by_avg_dep_delay
ABE,G4,1839,8.4312,0.6431,30,0.016313,12.1596,-3.7285,1
ABE,9E,1017,9.4177,0.6693,14,0.013766,12.1596,-2.7419,2
ABE,OH,1166,15.5465,4.446,15,0.012864,12.1596,3.3868,3
ABE,OO,315,30.6304,22.3077,12,0.038095,12.1596,18.4707,4
ABI,MQ,1757,7.3098,4.4095,15,0.008537,7.3098,0.0,1
ABQ,DL,1547,1.7462,-5.6026,14,0.00905,9.4674,-7.7211,1
ABQ,OO,3987,2.1028,-2.0512,18,0.004515,9.4674,-7.3646,2
ABQ,MQ,907,5.2841,3.2584,6,0.006615,9.4674,-4.1833,3
ABQ,UA,1822,5.4881,-0.3209,19,0.010428,9.4674,-3.9793,4

```

## 10m

### analysis_1

#### hive

```text
9E,BNA,1795,-43.0,1214.0,15.8782,57,0.031755,1,10,11,12,2,3,4,5,6,7,8,9
9E,BTR,747,-34.0,1015.0,5.4156,13,0.017403,1,10,11,12,2,3,5,6,7,8,9
9E,BTV,2523,-48.0,916.0,0.8223,67,0.026556,1,10,11,12,2,3,4,5,6,7,8,9
9E,CHO,2527,-43.0,1063.0,2.3155,64,0.025326,1,10,11,12,2,3,4,5,6,7,8,9
9E,CID,209,-35.0,129.0,-2.0287,0,0.0,1,10,11,4,5,9
9E,CRW,281,-36.0,149.0,-7.5587,0,0.0,1,10,11,12,3,4,9
9E,CSG,651,-37.0,1247.0,2.9795,18,0.02765,1,10,11,12,2,3,4,5,6,7,8,9
9E,DHN,792,-41.0,937.0,4.019,3,0.003788,1,10,11,12,2,3,4,5,6,9
9E,DLH,246,-27.0,241.0,3.791,2,0.00813,4,5,6,7,8,9
9E,EWR,2326,-50.0,1110.0,15.8615,75,0.032244,1,10,11,12,2,3,4,5,6,7,8,9

```

#### spark_core

```text
airline,origin,total_flights,min_arr_delay,max_arr_delay,avg_arr_delay,cancelled_flights,cancellation_rate,active_months
9E,DTW,18427,-46.0,941.0,0.377,158,0.008574,"1,2,3,4,5,6,7,8,9,10,11,12"
9E,BDL,611,-31.0,303.0,0.6107,15,0.02455,"1,2,3,4,5,6,7,8,9,10,12"
9E,FAY,467,-32.0,949.0,6.2077,0,0.0,"1,2,3,4,5,6,9,10,11,12"
9E,MLU,1181,-42.0,885.0,8.541,9,0.007621,"1,2,3,4,5,6,7,8,9,10,11,12"
9E,ROC,3813,-49.0,1184.0,1.059,115,0.03016,"1,2,3,4,5,6,7,8,9,10,11,12"
9E,LEX,364,-38.0,181.0,-2.8599,0,0.0,"1,2,3,4,5,11,12"
9E,LIT,362,-39.0,457.0,8.3775,6,0.016575,"1,2,3,4,6,7,8,9,10,11,12"
9E,GFK,136,-45.0,478.0,4.6397,0,0.0,"1,2,3,9,12"
9E,AVL,897,-43.0,949.0,3.0945,14,0.015608,"1,2,3,4,5,6,7,8,9,10,11,12"

```

#### spark_sql

```text
airline,origin,total_flights,min_arr_delay,max_arr_delay,avg_arr_delay,cancelled_flights,cancellation_rate,active_months
9E,ABE,1446,-47.0,575.0,-0.0014,16,0.011065,"1,10,11,12,2,3,4,5,6,7,8,9"
9E,ABY,46,-32.0,321.0,11.9783,0,0.0,"1,11,12,2,3"
9E,AEX,1190,-34.0,979.0,8.7029,11,0.009244,"1,10,11,12,2,3,4,5,6,7,8,9"
9E,AGS,2212,-36.0,1091.0,6.9251,33,0.014919,"1,10,11,12,2,3,4,5,6,7,8,9"
9E,ALB,1639,-51.0,394.0,-5.181,29,0.017694,"1,10,11,12,2,3,4,5,6,7,8,9"
9E,ATL,37532,-43.0,1207.0,2.5427,368,0.009805,"1,10,11,12,2,3,4,5,6,7,8,9"
9E,ATW,310,-34.0,420.0,5.411,0,0.0,"1,10,4,5,6,7,8,9"
9E,AUS,699,-35.0,1225.0,14.5733,3,0.004292,"1,11,2,3,4,5,6,7"
9E,AVL,897,-43.0,949.0,3.0945,14,0.015608,"1,10,11,12,2,3,4,5,6,7,8,9"

```

### analysis_2

#### hive

```text
ABE,1,high,60,241.3,234.0333,1:Delay_late_aircraft=28; 2:Delay_carrier=24; 3:Delay_nas=4
ABE,1,low,554,-5.509,-14.5564,1:Delay_nas=40; 2:Delay_carrier=2
ABE,1,medium,62,34.3226,32.5,1:Delay_late_aircraft=24; 2:Delay_carrier=16; 3:Delay_nas=6
ABE,2,high,28,227.9286,217.9286,1:Delay_carrier=12; 2:Delay_late_aircraft=12; 3:Delay_nas=2
ABE,2,low,594,-6.6498,-19.5709,1:Delay_nas=20; 2:Delay_carrier=2; 3:Delay_weather=2
ABE,2,medium,40,29.7,10.1053,1:Delay_carrier=10; 2:Delay_late_aircraft=6
ABE,3,high,46,173.4348,163.3913,1:Delay_carrier=18; 2:Delay_late_aircraft=16; 3:Delay_nas=12
ABE,3,low,678,-6.1858,-18.3687,1:Delay_nas=14
ABE,3,medium,56,30.6786,19.8929,1:Delay_late_aircraft=14; 2:Delay_carrier=8; 3:Delay_nas=8
ABE,4,high,58,258.6552,250.3793,1:Delay_carrier=32; 2:Delay_late_aircraft=14; 3:Delay_nas=8

```

#### spark_core

```text
origin,month,dep_delay_band,flight_count,avg_dep_delay,avg_arr_delay,top_3_causes
JFK,1,low,14466,-2.817,-14.054,1:Delay_nas=1168; 2:Delay_carrier=72; 3:Delay_late_aircraft=6
GRR,1,low,2196,-4.2177,-8.515,1:Delay_nas=274; 2:Delay_carrier=16; 3:Delay_late_aircraft=12
CLT,1,low,23610,-1.9366,-6.7901,1:Delay_nas=1274; 2:Delay_carrier=98; 3:Delay_late_aircraft=58
SYR,1,low,1738,-5.3579,-14.714,1:Delay_nas=136; 2:Cancellation_A=2; 3:Delay_carrier=2
MDT,1,low,580,-5.6793,-11.3391,1:Delay_nas=46; 2:Delay_weather=2
MYR,1,low,1298,-7.4453,-14.8875,1:Delay_nas=24; 2:Delay_late_aircraft=2
CWA,1,low,108,-5.5185,-15.6296,1:Delay_nas=2
GRB,1,low,466,-3.8026,-10.8798,1:Delay_nas=36; 2:Delay_carrier=4
CAE,1,low,772,-5.1166,-10.7461,1:Delay_nas=36; 2:Delay_late_aircraft=2

```

#### spark_sql

```text
origin,month,dep_delay_band,flight_count,avg_dep_delay,avg_arr_delay,top_3_causes
BGR,1,low,364,-7.4505,-18.8901,1:Delay_nas=18; 2:Delay_carrier=2
TYS,1,low,1640,-5.5744,-10.3187,1:Delay_nas=146; 2:Delay_carrier=8
VLD,1,low,108,-5.3519,-13.1111,NoCauseAvailable
ELP,1,high,128,164.6719,164.8906,1:Delay_late_aircraft=76; 2:Delay_carrier=28; 3:Delay_weather=16
AMA,1,high,60,173.9,168.5333,1:Delay_late_aircraft=38; 2:Delay_carrier=12; 3:Delay_weather=6
SMF,1,low,6818,-2.6709,-8.3452,1:Delay_nas=156; 2:Delay_carrier=62; 3:Delay_late_aircraft=6
LAX,1,high,1656,154.3514,147.8027,1:Delay_late_aircraft=776; 2:Delay_carrier=656; 3:Delay_nas=120
COS,1,low,1548,-3.3953,-6.5953,1:Delay_nas=92; 2:Delay_carrier=12; 3:Cancellation_A=2
ACY,1,medium,48,29.375,30.875,1:Delay_nas=18; 2:Delay_late_aircraft=10; 3:Delay_carrier=6

```

### analysis_3

#### hive

```text
ABE,G4,2557,9.1648,1.0092,33,0.012906,12.4369,-3.2721,1
ABE,9E,1446,9.3406,-0.0014,16,0.011065,12.4369,-3.0963,2
ABE,OH,1633,14.1819,3.4412,22,0.013472,12.4369,1.745,3
ABE,OO,581,30.1344,20.9891,23,0.039587,12.4369,17.6975,4
ABI,MQ,2503,8.753,6.2949,27,0.010787,8.753,0.0,1
ABQ,DL,2122,1.5251,-5.8949,14,0.006598,10.0162,-8.4911,1
ABQ,OO,5678,2.938,-1.1292,34,0.005988,10.0162,-7.0782,2
ABQ,MQ,1097,5.9171,3.9732,11,0.010027,10.0162,-4.0991,3
ABQ,UA,2501,6.4361,0.5628,26,0.010396,10.0162,-3.5801,4
ABQ,NK,720,8.5028,3.3876,8,0.011111,10.0162,-1.5134,5

```

#### spark_core

```text
origin,airline,total_flights,avg_dep_delay,avg_arr_delay,cancelled_flights,cancellation_rate,airport_avg_dep_delay,dep_delay_diff_from_airport,airport_rank_by_avg_dep_delay
OAK,HA,1389,-1.2172,-2.5381,32,0.023038,8.4653,-9.6826,1
OAK,OO,2208,2.8673,-0.5834,8,0.003623,8.4653,-5.5981,2
OAK,G4,173,3.2398,3.9357,2,0.011561,8.4653,-5.2256,3
OAK,AS,1035,4.1277,-2.3174,33,0.031884,8.4653,-4.3376,4
OAK,DL,785,4.3015,-5.3806,9,0.011465,8.4653,-4.1638,5
OAK,NK,3874,8.8868,4.4221,67,0.017295,8.4653,0.4215,6
OAK,WN,49622,9.1205,2.1232,277,0.005582,8.4653,0.6551,7
BOS,9E,16,-3.7143,-17.8571,2,0.125,11.7483,-15.4626,1
BOS,G4,685,3.1592,-5.6473,13,0.018978,11.7483,-8.5891,2

```

#### spark_sql

```text
origin,airline,total_flights,avg_dep_delay,avg_arr_delay,cancelled_flights,cancellation_rate,airport_avg_dep_delay,dep_delay_diff_from_airport,airport_rank_by_avg_dep_delay
ABE,G4,2557,9.1648,1.0092,33,0.012906,12.4369,-3.2721,1
ABE,9E,1446,9.3406,-0.0014,16,0.011065,12.4369,-3.0963,2
ABE,OH,1633,14.1819,3.4412,22,0.013472,12.4369,1.745,3
ABE,OO,581,30.1344,20.9891,23,0.039587,12.4369,17.6975,4
ABI,MQ,2503,8.753,6.2949,27,0.010787,8.753,0.0,1
ABQ,DL,2122,1.5251,-5.8949,14,0.006598,10.0162,-8.4911,1
ABQ,OO,5678,2.938,-1.1292,34,0.005988,10.0162,-7.0782,2
ABQ,MQ,1097,5.9171,3.9732,11,0.010027,10.0162,-4.0991,3
ABQ,UA,2501,6.4361,0.5628,26,0.010396,10.0162,-3.5801,4

```

## 14m

### analysis_1

#### hive

```text
9E,BDL,732,-31.0,303.0,1.5465,22,0.030055,1,10,12,2,3,4,5,6,7,8,9
9E,CID,320,-35.0,129.0,-2.6188,0,0.0,1,10,11,4,5,9
9E,FAY,698,-32.0,949.0,8.3696,0,0.0,1,10,11,12,2,3,4,5,6,9
9E,GFK,172,-45.0,478.0,10.9767,0,0.0,1,12,2,3,9
9E,LFT,1604,-42.0,1171.0,0.7382,20,0.012469,1,10,11,12,2,3,4,5,6,7,8,9
9E,MIA,30,-23.0,99.0,35.5333,0,0.0,1,12
9E,MYR,1094,-42.0,1011.0,-1.7782,26,0.023766,1,10,11,12,2,3,4,5,6,7,8,9
9E,ORF,4394,-43.0,1024.0,6.5738,120,0.02731,1,10,11,12,2,3,4,5,6,7,8,9
9E,SBN,22,-31.0,-9.0,-16.4545,0,0.0,1,10,11,12,9
9E,SGF,1272,-40.0,339.0,0.7242,6,0.004717,1,10,11,12,2,3,4,5,7,8,9

```

#### spark_core

```text
airline,origin,total_flights,min_arr_delay,max_arr_delay,avg_arr_delay,cancelled_flights,cancellation_rate,active_months
9E,JAX,1818,-52.0,1147.0,-0.1984,50,0.027503,"1,2,3,4,5,6,7,8,9,10,11,12"
9E,IND,4832,-48.0,1086.0,-1.0803,110,0.022765,"1,2,3,4,5,6,7,8,9,10,11,12"
9E,PHL,300,-37.0,371.0,-2.3,0,0.0,"1,2,3,11,12"
9E,FAY,698,-32.0,949.0,8.3696,0,0.0,"1,2,3,4,5,6,9,10,11,12"
9E,OAJ,1096,-39.0,1157.0,0.5657,0,0.0,"1,2,3,4,5,6,7,8,9,10,11,12"
9E,ICT,336,-34.0,204.0,1.9345,0,0.0,"1,2,3,11,12"
9E,OMA,994,-39.0,779.0,5.0166,30,0.030181,"1,2,3,4,5,6,7,8,9,10,11,12"
9E,CVG,13240,-56.0,1035.0,2.0709,230,0.017372,"1,2,3,4,5,6,7,8,9,10,11,12"
9E,XNA,3912,-44.0,894.0,0.2988,24,0.006135,"1,2,3,4,5,6,7,8,9,10,11,12"

```

#### spark_sql

```text
airline,origin,total_flights,min_arr_delay,max_arr_delay,avg_arr_delay,cancelled_flights,cancellation_rate,active_months
9E,ABE,2034,-47.0,575.0,0.6693,28,0.013766,"1,10,11,12,2,3,4,5,6,7,8,9"
9E,ABY,76,-32.0,321.0,4.3684,0,0.0,"1,11,12,2,3"
9E,AEX,1756,-34.0,979.0,9.6129,18,0.010251,"1,10,11,12,2,3,4,5,6,7,8,9"
9E,AGS,3206,-36.0,1091.0,6.9669,66,0.020586,"1,10,11,12,2,3,4,5,6,7,8,9"
9E,ALB,2178,-51.0,394.0,-4.3889,42,0.019284,"1,10,11,12,2,3,4,5,6,7,8,9"
9E,ATL,53754,-43.0,1207.0,2.4584,586,0.010902,"1,10,11,12,2,3,4,5,6,7,8,9"
9E,ATW,352,-34.0,420.0,9.3943,0,0.0,"1,10,4,5,6,7,8,9"
9E,AUS,758,-35.0,1225.0,14.1459,4,0.005277,"1,11,2,3,4,5,6,7"
9E,AVL,1350,-43.0,949.0,1.9164,28,0.020741,"1,10,11,12,2,3,4,5,6,7,8,9"

```

### analysis_2

#### hive

```text
ABE,1,high,60,241.3,234.0333,1:Delay_late_aircraft=28; 2:Delay_carrier=24; 3:Delay_nas=4
ABE,1,low,554,-5.509,-14.5564,1:Delay_nas=40; 2:Delay_carrier=2
ABE,1,medium,62,34.3226,32.5,1:Delay_late_aircraft=24; 2:Delay_carrier=16; 3:Delay_nas=6
ABE,2,high,28,227.9286,217.9286,1:Delay_carrier=12; 2:Delay_late_aircraft=12; 3:Delay_nas=2
ABE,2,low,594,-6.6498,-19.5709,1:Delay_nas=20; 2:Delay_carrier=2; 3:Delay_weather=2
ABE,2,medium,40,29.7,10.1053,1:Delay_carrier=10; 2:Delay_late_aircraft=6
ABE,3,high,46,173.4348,163.3913,1:Delay_carrier=18; 2:Delay_late_aircraft=16; 3:Delay_nas=12
ABE,3,low,678,-6.1858,-18.3687,1:Delay_nas=14
ABE,3,medium,56,30.6786,19.8929,1:Delay_late_aircraft=14; 2:Delay_carrier=8; 3:Delay_nas=8
ABE,4,high,58,258.6552,250.3793,1:Delay_carrier=32; 2:Delay_late_aircraft=14; 3:Delay_nas=8

```

#### spark_core

```text
origin,month,dep_delay_band,flight_count,avg_dep_delay,avg_arr_delay,top_3_causes
MSP,1,low,15108,-2.5821,-12.5667,1:Delay_nas=768; 2:Delay_carrier=216; 3:Delay_late_aircraft=12
TYS,1,low,1640,-5.5744,-10.3187,1:Delay_nas=146; 2:Delay_carrier=8
LGA,1,medium,2908,32.6651,27.3873,1:Delay_late_aircraft=844; 2:Delay_carrier=698; 3:Delay_nas=292
MYR,1,low,1298,-7.4453,-14.8875,1:Delay_nas=24; 2:Delay_late_aircraft=2
ROA,1,low,362,-4.2099,-8.663,1:Delay_nas=20; 2:Delay_carrier=2
ALB,1,low,1338,-3.5889,-9.5865,1:Delay_nas=112; 2:Delay_carrier=4; 3:Delay_late_aircraft=2
BUR,1,low,3824,-3.4854,-8.2499,1:Delay_nas=142; 2:Delay_carrier=40; 3:Delay_late_aircraft=10
BOS,1,high,1858,150.4596,150.9004,1:Delay_late_aircraft=786; 2:Delay_carrier=710; 3:Delay_weather=206
EGE,1,medium,242,35.0992,34.7686,1:Delay_late_aircraft=92; 2:Delay_carrier=64; 3:Delay_nas=32

```

#### spark_sql

```text
origin,month,dep_delay_band,flight_count,avg_dep_delay,avg_arr_delay,top_3_causes
BGR,1,low,364,-7.4505,-18.8901,1:Delay_nas=18; 2:Delay_carrier=2
TYS,1,low,1640,-5.5744,-10.3187,1:Delay_nas=146; 2:Delay_carrier=8
VLD,1,low,108,-5.3519,-13.1111,NoCauseAvailable
ELP,1,high,128,164.6719,164.8906,1:Delay_late_aircraft=76; 2:Delay_carrier=28; 3:Delay_weather=16
AMA,1,high,60,173.9,168.5333,1:Delay_late_aircraft=38; 2:Delay_carrier=12; 3:Delay_weather=6
SMF,1,low,6818,-2.6709,-8.3452,1:Delay_nas=156; 2:Delay_carrier=62; 3:Delay_late_aircraft=6
LAX,1,high,1656,154.3514,147.8027,1:Delay_late_aircraft=776; 2:Delay_carrier=656; 3:Delay_nas=120
COS,1,low,1548,-3.3953,-6.5953,1:Delay_nas=92; 2:Delay_carrier=12; 3:Cancellation_A=2
ACY,1,medium,48,29.375,30.875,1:Delay_nas=18; 2:Delay_late_aircraft=10; 3:Delay_carrier=6

```

### analysis_3

#### hive

```text
ABE,G4,3678,8.4312,0.6431,60,0.016313,12.1596,-3.7285,1
ABE,9E,2034,9.4177,0.6693,28,0.013766,12.1596,-2.7419,2
ABE,OH,2332,15.5465,4.446,30,0.012864,12.1596,3.3868,3
ABE,OO,630,30.6304,22.3077,24,0.038095,12.1596,18.4707,4
ABI,MQ,3514,7.3098,4.4095,30,0.008537,7.3098,0.0,1
ABQ,DL,3094,1.7462,-5.6026,28,0.00905,9.4674,-7.7211,1
ABQ,OO,7974,2.1028,-2.0512,36,0.004515,9.4674,-7.3646,2
ABQ,MQ,1814,5.2841,3.2584,12,0.006615,9.4674,-4.1833,3
ABQ,UA,3644,5.4881,-0.3209,38,0.010428,9.4674,-3.9793,4
ABQ,AS,846,8.4024,4.5263,8,0.009456,9.4674,-1.065,5

```

#### spark_core

```text
origin,airline,total_flights,avg_dep_delay,avg_arr_delay,cancelled_flights,cancellation_rate,airport_avg_dep_delay,dep_delay_diff_from_airport,airport_rank_by_avg_dep_delay
DFW,MQ,140004,8.7894,4.7399,2200,0.015714,18.9336,-10.1442,1
DFW,OO,48822,9.8556,5.7204,982,0.020114,18.9336,-9.078,2
DFW,DL,24438,14.4578,6.8481,226,0.009248,18.9336,-4.4758,3
DFW,UA,16536,14.9894,10.8014,258,0.015602,18.9336,-3.9442,4
DFW,AS,4808,15.0509,13.6149,106,0.022047,18.9336,-3.8827,5
DFW,NK,20250,17.7148,11.7358,264,0.013037,18.9336,-1.2188,6
DFW,OH,18492,20.3167,15.3249,468,0.025308,18.9336,1.3831,7
DFW,F9,20420,21.377,20.1415,546,0.026738,18.9336,2.4434,8
DFW,AA,332572,24.9422,19.29,6614,0.019887,18.9336,6.0086,9

```

#### spark_sql

```text
origin,airline,total_flights,avg_dep_delay,avg_arr_delay,cancelled_flights,cancellation_rate,airport_avg_dep_delay,dep_delay_diff_from_airport,airport_rank_by_avg_dep_delay
ABE,G4,3678,8.4312,0.6431,60,0.016313,12.1596,-3.7285,1
ABE,9E,2034,9.4177,0.6693,28,0.013766,12.1596,-2.7419,2
ABE,OH,2332,15.5465,4.446,30,0.012864,12.1596,3.3868,3
ABE,OO,630,30.6304,22.3077,24,0.038095,12.1596,18.4707,4
ABI,MQ,3514,7.3098,4.4095,30,0.008537,7.3098,0.0,1
ABQ,DL,3094,1.7462,-5.6026,28,0.00905,9.4674,-7.7211,1
ABQ,OO,7974,2.1028,-2.0512,36,0.004515,9.4674,-7.3646,2
ABQ,MQ,1814,5.2841,3.2584,12,0.006615,9.4674,-4.1833,3
ABQ,UA,3644,5.4881,-0.3209,38,0.010428,9.4674,-3.9793,4

```

