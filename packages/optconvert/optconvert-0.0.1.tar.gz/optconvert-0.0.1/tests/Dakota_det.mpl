TITLE
    
    DakotaModel_deterministic;
    ! Objective value 4165.0

INDEX

    PRODUCTS := (Desk, Table, Chair);
    RESOURCES := (Lumber, Finishing, Carpentry);

DATA

    Price[PRODUCTS] := (60, 40, 10);
    Cost[RESOURCES] := (2, 4, 5.2);
    Consumption[RESOURCES, PRODUCTS] := (8, 6, 1
					4, 2, 1.5
					2, 1.5, .5);
    Demand[PRODUCTS] := (150, 125, 300);

BINARY VARIABLES

   BinVec[PRODUCTS];


VARIABLES

   Purchase[RESOURCES];
   Production[PRODUCTS];
   BinaryVar;

MIN

    Profit = -sum(PRODUCTS: Price * Production) + sum(RESOURCES: Cost * Purchase) - BinaryVar - sum(PRODUCTS: BinVec);

SUBJECT TO

    ResourceConstraint[RESOURCES]: sum(PRODUCTS: Consumption * Production) <= Purchase;
    DemandConstraint[PRODUCTS]: Production <= Demand;

BOUNDS

    DeskBound: Production[PRODUCTS=Desk] <= 160 ;
    TableBound: 130 >= Production[PRODUCTS=Table] ;

FREE

    Purchase[RESOURCES=Lumber];

BINARY

   BinaryVar;

INTEGER

   Production[PRODUCTS];

END