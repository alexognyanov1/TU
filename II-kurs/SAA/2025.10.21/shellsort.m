function outv = shellsort(a)
  n = length(a);
  gap = [1 4 13 40 121 364 1093 3280]; % gap = 3*k+1
  l = length(gap);
  for i = l:-1:1
      flag = 0;
      while ~flag
      flag = 1;
          for j = n-gap(i):-1:1
              if a(j) > a(j+gap(i))
                      tmp = a(j);
                      a(j) = a(j+gap(i));
                      a(j+gap(i)) = tmp;
                      flag = 0;
              end
          end;
      end
  end
  outv = a;
end

