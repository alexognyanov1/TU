#include <stdio.h>

int main() {
  int N, M;
  double exchangeRate;
  scanf("%d %d %lf", &N, &M, &exchangeRate);

  double monthlySalary = N * M;
  double yearlySalary = monthlySalary * 12;
  double bonus = 2.5 * monthlySalary;
  double totalIncome = yearlySalary + bonus;
  double afterTaxIncome = totalIncome * 0.75;
  double dailyIncomeInLeva = (afterTaxIncome / 365) * exchangeRate;

  printf("%.2lf\n", dailyIncomeInLeva);
  return 0;
}