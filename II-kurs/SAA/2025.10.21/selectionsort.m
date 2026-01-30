function outv = selectionsort(v)
  n = length(v);

  for i = 1:n-1
      minIndex = i;

      for j = i+1:n
          if v(j) < v(minIndex)
              minIndex = j;
          end
      end

      if minIndex ~= i
          temp = v(i);
          v(i) = v(minIndex);
          v(minIndex) = temp;
      end
  end

  outv = v;

end

