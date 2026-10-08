
grafo([
    nodo(vancouver, [vecino(edmonton, 16), vecino(calgary, 13)]),
    nodo(calgary,   [vecino(edmonton, 4),  vecino(regina, 14)]),
    nodo(edmonton,  [vecino(saskatoon, 12)]),
    nodo(saskatoon, [vecino(calgary, 9),   vecino(winnipeg, 20)]),
    nodo(regina,    [vecino(saskatoon, 7), vecino(winnipeg, 4)]),
    nodo(winnipeg,  [])
]).

% REGLAS
conexion(Origen, Destino, Costo) :-
    grafo(ListaNodos),
    member(nodo(Origen, Vecinos), ListaNodos),
    member(vecino(Destino, Costo), Vecinos).


tiene_aristas(Nodo) :-
    conexion(Nodo, _, _) ; conexion(_, Nodo, _).


costo_pasando_por(X, Y, Z, CostoTotal) :-
    conexion(X, Y, Costo1),
    conexion(Y, Z, Costo2),
    CostoTotal is Costo1 + Costo2.

viaje(X, Y) :-
    viaje_aux(X, Y, [X]).

%función auxiliar que verifica los nodos ya visitados
viaje_aux(X, Y, _Visitados) :-
    conexion(X, Y, _).

viaje_aux(X, Y, Visitados) :-
    conexion(X, Z, _),
    \+ member(Z, Visitados),
    viaje_aux(Z, Y, [Z | Visitados]).

/** <examples>
?- conexion(saskatoon, vancouver, Costo).
?- conexion(regina, Nodo, Costo).
?- viaje(edmonton, calgary)
*/