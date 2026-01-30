function outv = insertionsort(v)
  n = length(v);

  for i = 2:n
      key = v(i);
      j = i - 1;

      while j >= 1 && v(j) > key
          v(j + 1) = v(j);
          j = j - 1;
      end

      v(j + 1) = key;
  end

  outv = v;

end
