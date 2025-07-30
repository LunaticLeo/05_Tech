-module(try_erlang).
%% -export([start/0,while/1,while/2]).
-compile(export_all).
-include_lib("./try_erlang.hrl").

% consumer (Id , Buffer ) ->
%     timer : sleep (200) ,
%     io: fwrite (" Consumer ~p trying to consume ~n",[Id]),
%     Ref = make_ref (),
%     Buffer !{ start_consume , self (), Ref },
%     receive
%     { ok_to_consume , Ref} ->
%         io: fwrite (" Consumer ~p consuming ~n",[Id]),
%         Buffer !{ end_consume },
%         io: fwrite (" Consumer ~p stopped consuming ~n",[Id]),
%         consumer (Id , Buffer )
%     end.

% producer (Id , Buffer ) ->
%     timer : sleep (1000) ,
%     io: fwrite (" Producer ~p trying to produce ~n",[Id]),
%     Ref = make_ref (),
%     Buffer !{ start_produce , self (), Ref },
%     receive
%         { ok_to_produce , Ref} ->
%             io: fwrite (" Producer ~p producing ~n",[Id]),
%             Buffer !{ end_produce },
%             io: fwrite (" Producer ~p stopped producing ~n",[Id]),
%             producer (Id , Buffer )
% end.


% loopPC (Cs , Ps , MaxBufferSize , OccupiedSlots ) ->
% %% implement me
%     receive
%         {start_consume, From, _} when OccupiedSlots>0 ->
%             From ! {ok_to_consume},
%             loopPC(Cs+1,Ps, MaxBufferSize,OccupiedSlots);
%         {start_produce, From, _} when OccupiedSlots<MaxBufferSize ->
%             From ! {ok_to_produce};
%         {end_produce} ->
%             OccupiedSlots = OccupiedSlots +1;
%         {end_consume} ->
%             OccupiedSlots = OccupiedSlots -1
% end.

% startPC () ->
%     Buffer = spawn ( fun () -> loopPC (0 ,0 ,10 ,0) end ),
%     [ spawn ( fun () -> producer (Id , Buffer ) end ) || Id <- lists : seq (1 ,10)],
%     [ spawn ( fun () -> consumer (Id , Buffer ) end ) || Id <- lists : seq (1 ,10)].


send()->
    Pid = spawn(fun get/0),
    self() ! {msg},
    receive
        {msg} ->
            io:fwrite(getFromSelf)
end.

get() ->
    A=0,
    receive
        {msg} when A>0 ->
            io:fwrite(looksGood)
end.
