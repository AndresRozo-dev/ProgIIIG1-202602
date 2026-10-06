
conexion(vancouver, edmonton, 16).
conexion(vancouver, calgary, 13).
conexion(calgary, edmonton, 4).
conexion(edmonton, saskatoon, 12).
conexion(saskatoon, calgary, 9).
conexion(saskatoon, winnipeg, 20).
conexion(calgary, regina, 14).
conexion(regina, saskatoon, 7).
conexion(regina, winnipeg, 4).


tiene_aristas(Nodo) :- 
    conexion(Nodo, _, _); 
    conexion(_, Nodo, _).

costo_pasando_por(X, Y, Z, CostoTotal) :-
    conexion(X, Y, Costo1),
    conexion(Y, Z, Costo2),
    CostoTotal is Costo1 + Costo2.




viaje(X, Y) :-
    viaje_aux(X, Y, [X]).


%caso base
viaje_aux(X, Y, _Visitados) :- 
    conexion(X, Y, _).

% Regla recursiva
viaje_aux(X, Y, Visitados) :- 
    conexion(X, Z, _), 
   	\+ member(Z, Visitados),
    viaje_aux(Z, Y, [Z | Visitados]).




/** <examples>
?- conexion(saskatoon, vancouver, Costo).
?- conexion(regina, Nodo, Costo).
*/
