function outv = bubblesortFlag(v)
n = length(v);

for i = 1:n-1
    swapped = false;

    for j = 1:n-i
        if v(j) > v(j+1)
            temp = v(j);
            v(j) = v(j+1);
            v(j+1) = temp;
            swapped = true;
        end
    end
    if ~swapped
        break;
    end
end

outv = v;

end

