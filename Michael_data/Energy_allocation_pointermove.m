function Newpointer=Energy_allocation_pointermove(Memopointer,S_memo)
% S_memo已设置为常数，这玩意就是从1-8000循环记录，够了8000再从1开始记录
if Memopointer<S_memo
    Newpointer=Memopointer+1;
else
    Newpointer=1;
end