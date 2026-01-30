u = randi([1 10000],1,10000);

tic;
bs = bubblesort(u);
toc;

tic;
ss = selectionsort(u);
toc;


tic;
bsf = insertionsort(u);
toc;

