from __future__ import print_function, division, absolute_import

#### Correlators prior from theory (Danny sent by mail)

#  - B->K^*ccbar::Re{alpha_0^perp}@BCvDV2016
#  - B->K^*ccbar::Re{alpha_0^para}@BCvDV2016
#  - B->K^*ccbar::Re{alpha_0^long}@BCvDV2016
#  - B->K^*ccbar::Im{alpha_0^perp}@BCvDV2016
#  - B->K^*ccbar::Im{alpha_0^para}@BCvDV2016
#  - B->K^*ccbar::Im{alpha_0^long}@BCvDV2016
#  - B->K^*ccbar::Re{alpha_1^perp}@BCvDV2016
#  - B->K^*ccbar::Re{alpha_1^para}@BCvDV2016
#  - B->K^*ccbar::Re{alpha_1^long}@BCvDV2016
#  - B->K^*ccbar::Im{alpha_1^perp}@BCvDV2016
#  - B->K^*ccbar::Im{alpha_1^para}@BCvDV2016
#  - B->K^*ccbar::Im{alpha_1^long}@BCvDV2016
#  - B->K^*ccbar::Re{alpha_2^perp}@BCvDV2016
#  - B->K^*ccbar::Re{alpha_2^para}@BCvDV2016
#  - B->K^*ccbar::Im{alpha_2^perp}@BCvDV2016
#  - B->K^*ccbar::Im{alpha_2^para}@BCvDV2016

param_mean_H = [ -5.72780617508e-06,
                 -3.44899546179e-05,
                  5.26100890954e-06,
                 -2.09103377246e-05,
                 -4.22060859862e-06,
                 -4.70470229701e-06,
                 -0.000676717804637,
                 -0.00031304395992 ,
                  0.00172639919484 ,
                  0.000116510029519,
                 -0.00021407138014 ,
                  0.000429344452893,
                  0.00189631069765 ,
                  0.00121955990214 ,
                 -7.71396357554e-06,
                  0.000602973160164 ]

param_sigma_H = [ 2.08371498722e-05,
                  2.71313696616e-05,
                  5.86272439926e-05,
                  6.18438152254e-05,
                  4.06438148419e-05,
                  0.000134166507639,
                  0.00015207421219 ,
                  0.000164013890819,
                  0.000224817863748,
                  0.000358159017491,
                  0.000223477273046,
                  0.00036728858819 ,
                  0.000245567466708,
                  0.000249603007396,
                  0.000498873002304,
                  0.000314059063727 ]

correlations_H = [
    [ 1.0, 0.157640049178, -0.192053075729, 0.144883341936, 0.206736678669, -0.196764394091, -0.910040974814, -0.119334421509, 0.158073926034, -0.132657252708, -0.173562869237, 0.204567585349, 0.792628513106, 0.0845034341842, 0.120373583131, 0.14090168862 ],
    [ 0.157640049178, 1.0, -0.523153849804, -0.701188081018, -0.64839723491, 0.653293252682, -0.038888778712, -0.8894459441, 0.306310499639, 0.636738353479, 0.581513934399, -0.508017018543, -0.0149338604785, 0.734079737164, -0.574538981864, -0.497318099244 ],
    [ -0.192053075729, -0.523153849804, 1.0, 0.49102848275, 0.396295108356, -0.474571804458, 0.103435556766, 0.405845939214, -0.545718225369, -0.417267671359, -0.283355041199, 0.378874701526, -0.0600164845596, -0.309874052979, 0.359244017986, 0.197272102404 ],
    [ 0.144883341936, -0.701188081018, 0.49102848275, 1.0, 0.878609367819, -0.862018810884, -0.171547791804, 0.59375027858, -0.298932780545, -0.949491407063, -0.753975474092, 0.677549128738, 0.172126750093, -0.485204707506, 0.878296785485, 0.623300532777],
    [ 0.206736678669, -0.64839723491, 0.396295108356, 0.878609367819, 1.0, -0.819788200348, -0.207718992685, 0.568980253075, -0.201452851903, -0.79402930837, -0.91224625899, 0.605519508965, 0.196032709599, -0.476419091369, 0.713481946192, 0.783596875979 ],
    [ -0.196764394091, 0.653293252682, -0.474571804458, -0.862018810884, -0.819788200348, 1.0, 0.222396493135, -0.494355062204, 0.279399678185, 0.712504878113, 0.602840402557, -0.781449977809, -0.219584785717, 0.369619538517, -0.600879662304, -0.432946041025 ],
    [ -0.910040974814, -0.038888778712, 0.103435556766, -0.171547791804, -0.207718992685, 0.222396493135, 1.0, 0.130525209944, -0.239597844538, 0.153298828548, 0.203587526505, -0.239044424594, -0.962994517777, -0.165061360246, -0.137588518472, -0.186008102289 ],
    [ -0.119334421509, -0.8894459441, 0.405845939214, 0.59375027858, 0.568980253075, -0.494355062204, 0.130525209944, 1.0, -0.38431776786, -0.604869875434, -0.560930390766, 0.475358840277, -0.125537673205, -0.953335361933, 0.584365321264, 0.510358844655 ],
    [ 0.158073926034, 0.306310499639, -0.545718225369, -0.298932780545, -0.201452851903, 0.279399678185, -0.239597844538, -0.38431776786, 1.0, 0.316132122324, 0.162240761621, -0.297875826934, 0.267946434981, 0.400282765031, -0.310334619486, -0.125143075103 ],
    [ -0.132657252708, 0.636738353479, -0.417267671359, -0.949491407063, -0.79402930837, 0.712504878113, 0.153298828548, -0.604869875434, 0.316132122324, 1.0, 0.780800441699, -0.692839887436, -0.153302169147, 0.531957745243, -0.982309576433, -0.710786892586 ],
    [ -0.173562869237, 0.581513934399, -0.283355041199, -0.753975474092, -0.91224625899, 0.602840402557, 0.203587526505, -0.560930390766, 0.162240761621, 0.780800441699, 1.0, -0.588058082165, -0.205029297067, 0.496582408007, -0.761367933823, -0.965320024414 ],
    [ 0.204567585349, -0.508017018543, 0.378874701526, 0.677549128738, 0.605519508965, -0.781449977809, -0.239044424594, 0.475358840277, -0.297875826934, -0.692839887436, -0.588058082165, 1.0, 0.242108064378, -0.411698607931, 0.671574381546, 0.532170578774 ],
    [ 0.792628513106, -0.0149338604785, -0.0600164845596, 0.172126750093, 0.196032709599, -0.219584785717, -0.962994517777, -0.125537673205, 0.267946434981, -0.153302169147, -0.205029297067, 0.242108064378, 1.0, 0.195375559357, 0.138136310401, 0.196132745974 ],
    [ 0.0845034341842, 0.734079737164, -0.309874052979, -0.485204707506, -0.476419091369, 0.369619538517, -0.165061360246, -0.953335361933, 0.400282765031, 0.531957745243, 0.496582408007, -0.411698607931, 0.195375559357, 1.0, -0.53308440695, -0.465721116248 ],
    [ 0.120373583131, -0.574538981864, 0.359244017986, 0.878296785485, 0.713481946192, -0.600879662304, -0.137588518472, 0.584365321264, -0.310334619486, -0.982309576433, -0.761367933823, 0.671574381546, 0.138136310401, -0.53308440695, 1.0, 0.728086830099 ],
    [ 0.14090168862, -0.497318099244, 0.197272102404, 0.623300532777, 0.783596875979, -0.432946041025, -0.186008102289, 0.510358844655, -0.125143075103, -0.710786892586, -0.965320024414, 0.532170578774, 0.196132745974, -0.465721116248, 0.728086830099, 1.0 ],
    ]


