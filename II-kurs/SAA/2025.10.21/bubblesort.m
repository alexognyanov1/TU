function outv = bubblesort(v)
n = length(v);

for i = 1:n-1
    for j = 1:n-i
        if v(j) > v(j+1)
            temp = v(j);
            v(j) = v(j+1);
            v(j+1) = temp;
        end
    end
end

outv = v;

end

