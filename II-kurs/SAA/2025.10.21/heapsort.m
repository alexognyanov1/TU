function outv = heapsort(v)
n = length(v);
L = floor(n/2); R = n;

while L >= 1
    v = sift_heap(v, L, n);
    L = L - 1;
end

R = n;
while R > 1
    temp = v(1);
    v(1) = v(R);
    v(R) = temp;

    R = R - 1;
    v = sift_heap(v, 1, R);
end

outv = v;

end

function a = sift_heap(a,L,R)
i = L; j = 2*L; x = a(L);
while j <= R
    if j < R && a(j) < a(j+1)
        j = j + 1;
    end
    if x >= a(j)
        break
    end
    a(i) = a(j);
    i = j;
    j = 2*i;
end
a(i) = x;
end

