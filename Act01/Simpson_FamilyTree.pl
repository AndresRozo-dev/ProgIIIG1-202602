:- discontiguous padre_de/2.
:- discontiguous madre_de/2.

padre_de(abraham, homero).
madre_de(mona, homero).

padre_de(abraham, herbert).

padre_de(clancy, marge).
madre_de(jacqueline, marge).

padre_de(clancy, patty).
madre_de(jacqueline, patty).

padre_de(clancy, selma).
madre_de(jacqueline, selma).

padre_de(homero, bart).
madre_de(marge, bart).

padre_de(homero, lisa).
madre_de(marge, lisa).

padre_de(homero, maggie).
madre_de(marge, maggie).

madre_de(selma, ling).

progenitor_de(Padre, Hijo):-
    padre_de(Padre, Hijo); madre_de(Padre, Hijo).

abuelo_de(Abuelo, Nieto):-
    (    padre_de(Abuelo, Padre), padre_de(Padre, Nieto));
    (   padre_de(Abuelo, Madre), madre_de(Madre, Nieto)).

abuela_de(Abuela, Nieto):-
    (    madre_de(Abuela, Padre), padre_de(Padre, Nieto));
    (   madre_de(Abuela, Madre), madre_de(Madre, Nieto)).

nieto_de(Nieto, Abuelo):-
    abuelo_de(Abuelo, Nieto);
    abuela_de(Abuelo, Nieto).

hermano_de(Hermano1, Hermano2):-
    progenitor_de(Padre, Hermano1), 
   	progenitor_de(Padre, Hermano2),
    Hermano1 \= Hermano2.

tio_de(Tio, Sobrino):-
    progenitor_de(Padre, Sobrino), 
    hermano_de(Padre, Tio).

sobrino_de(Sobrino, Tio):-
    tio_de(Tio, Sobrino).

primo_de(Primo1, Primo2):-
	progenitor_de(Padre1, Primo1), 
    progenitor_de(Padre2, Primo2),
    hermano_de(Padre1, Padre2).



/** <examples>
?- abuelo_de(X, bart)
?- tio_de(X, lisa)
?- nieto_de(X, abraham)
?- hermano_de(X, ling)
?- primo_de(maggie, ling)
?- sobrino_de(X, herbert)
*/
