%  La ley dice que es un crimen para un Estadounidense vender armas a naciones
%  hostiles. Corea del Sur, enemigo de Estados Unidos, tiene algunos misiles, y todos
%  sus misiles les fueron vendidos por el Coronel West, quien es Estadounidense.
%  Pruebe que el Col. West es un criminal.

estadounidense(west).
son_enemigos(estados_unidos, surcorea).
tiene_misiles(surcorea).
vender_armas(west, surcorea).

pais_hostil_de(Pais1, Pais_hostil):-
    tiene_misiles(Pais_hostil),
    son_enemigos(Pais1,Pais_hostil).

es_criminal_estadounidense(Persona):-
    estadounidense(Persona),
    vender_armas(Persona, Pais),
    pais_hostil_de(estados_unidos, Pais).
    

/** <examples>
?- es_criminal_estadounidense(west)
*/
