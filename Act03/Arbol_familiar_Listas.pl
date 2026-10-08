familia([
    persona(abraham, masculino, [homero, herbert]),
    persona(mona, femenino, [homero]),
    persona(clancy, masculino, [marge, patty, selma]),
    persona(jacqueline, femenino, [marge, patty, selma]),
    persona(homero, masculino, [bart, lisa, maggie]),
    persona(marge, femenino, [bart, lisa, maggie]),
    persona(selma, femenino, [ling]),
    persona(herbert, masculino, []),
    persona(patty, femenino, []),
    persona(bart, masculino, []),
    persona(lisa, femenino, []),
    persona(maggie, femenino, []),
    persona(ling, femenino, [])
]).

miembro_familia(Persona) :-
    familia(ListaFamilia),
    member(Persona, ListaFamilia).

progenitor_de(Progenitor, Hijo) :-
    miembro_familia(persona(Progenitor, _, Hijos)),
    member(Hijo, Hijos).

madre_de(Madre, Hijo) :-
    miembro_familia(persona(Madre, femenino, Hijos)),
    member(Hijo, Hijos).

padre_de(Padre, Hijo) :-
    miembro_familia(persona(Padre, masculino, Hijos)),
    member(Hijo, Hijos).



abuela_de(Abuela, Nieto) :-
    madre_de(Abuela, Progenitor),
    progenitor_de(Progenitor, Nieto).

abuelo_de(Abuelo, Nieto) :-
    padre_de(Abuelo, Progenitor),
    progenitor_de(Progenitor, Nieto).

nieto_de(Nieto, Abuelo) :-
    abuelo_de(Abuelo, Nieto) ; abuela_de(Abuelo, Nieto).

hermano_de(Hermano1, Hermano2) :-
    progenitor_de(Padre, Hermano1),
    progenitor_de(Padre, Hermano2),
    Hermano1 \= Hermano2.

tio_de(Tio, Sobrino) :-
    progenitor_de(Padre, Sobrino),
    hermano_de(Padre, Tio).

sobrino_de(Sobrino, Tio) :-
    tio_de(Tio, Sobrino).

primo_de(Primo1, Primo2) :-
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
    
    
    