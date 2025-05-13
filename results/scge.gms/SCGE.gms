Set region(*);
Parameter alpha / 0.3 /;
Parameter rho / 0.5 /;
Parameter L(region);
Parameter K_total / 200.0 /;
positive Variable Y(region) / /;
positive Variable K(region) / /;
positive Variable C(region);
free Variable U / /;
free Variable Z / /;
Equation obj;
Equation eq_prod(region) / /;
Equation kap_constraint;
Equation eq_cons(region) / /;
Equation eq_utility;
Model SCGE / obj,eq_prod,kap_constraint,eq_cons,eq_utility /;
$onMultiR
$gdxLoadAll C:\Users\user\OneDrive\Desktop\scge-project\results\scge.gms\SCGE_data.gdx
$offMulti
obj .. Z =e= U;
eq_prod(region) .. Y(region) =e= (( rPower(L(region),alpha) ) * ( rPower(K(region),(1 - alpha)) ));
kap_constraint .. sum(region,K(region)) =e= K_total;
eq_cons(region) .. C(region) =e= Y(region);
eq_utility .. U =e= ( rPower(sum(region,( rPower(C(region),rho) )),(1 / rho)) );
solve SCGE using NLP MAX Z;