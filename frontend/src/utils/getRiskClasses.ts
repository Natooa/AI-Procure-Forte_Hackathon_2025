export const getRiskClasses = (risk: string) => {
  switch (risk) {
    case "низкий":
      return "bg-[var(--chart-2)] text-[var(--background)]";
    case "средний":
      return "bg-[var(--chart-3)] text-[var(--background)]";
    case "высокий":
      return "bg-[var(--chart-5)] text-[var(--background)]";
    default:
      return "";
  }
};
