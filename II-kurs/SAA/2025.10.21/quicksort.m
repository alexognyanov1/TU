function outv = quicksort(v)
%--------------------------------------------------------------------------
%
% Inputs:       v is a vector of length n
%
% Outputs:      outv is the sorted (ascending) version of v
%
% Description:  This function sorts the input array v in ascending order
%               using the quicksort algorithm
%
% Complexity:   O(n * log(n))    best-case performance
%               O(n * log(n))    average-case performance
%               O(n^2)           worst-case performance
%               O(log(n))        auxiliary space (stack)
%--------------------------------------------------------------------------

% Quicksort
n = length(v);
outv = sort(v,1,n);

end

function a = sort(a,L,R)
i = L; j = R; Pivot = a(floor((L+R)/2));
while i <= j
    while a(i) < Pivot
        i = i + 1;
    end
    while a(j) > Pivot
        j = j - 1;
    end
    if i <= j
        tmp = a(i); a(i) = a(j); a(j) = tmp; i = i + 1; j = j - 1;
    end
end

if L < j
    a = sort(a,L,j);
end
if i < R
    a = sort(a,i,R);
end
end


