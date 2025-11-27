import { Card } from "@/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { mockTenders } from "../Tender/mockTenders";

import {
  BarChart,
  Bar,
  CartesianGrid,
  XAxis,
  Cell,
  YAxis,
  PieChart,
  Pie,
  Legend,
} from "recharts";
import {
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
  ChartLegend,
  ChartLegendContent,
  type ChartConfig,
} from "@/components/ui/chart";
import { getRiskClasses } from "@/utils/getRiskClasses";
import { TendersTable } from "../Tender/TendersTable";

export default function DashboardPage() {
  const topTenders = mockTenders.slice(0, 5);
  // 1. Количество тендеров по риску
  const riskCounts = {
    низкий: mockTenders.filter((t) => t.risk === "низкий").length,
    средний: mockTenders.filter((t) => t.risk === "средний").length,
    высокий: mockTenders.filter((t) => t.risk === "высокий").length,
  };

  const chartRiskData = [
    { risk: "Низкий", count: riskCounts["низкий"] },
    { risk: "Средний", count: riskCounts["средний"] },
    { risk: "Высокий", count: riskCounts["высокий"] },
  ];

  const chartRiskConfig = {
    count: { label: "Количество тендеров", color: "var(--chart-3)" },
  } satisfies ChartConfig;

  const riskColors: Record<string, string> = {
    Низкий: "var(--chart-2)",
    Средний: "var(--chart-3)",
    Высокий: "var(--chart-5)",
  };

  // 2. Сумма цен по риску
  const chartPriceData = [
    {
      risk: "Низкий",
      price: mockTenders
        .filter((t) => t.risk === "низкий")
        .reduce((sum, t) => sum + t.price, 0),
    },
    {
      risk: "Средний",
      price: mockTenders
        .filter((t) => t.risk === "средний")
        .reduce((sum, t) => sum + t.price, 0),
    },
    {
      risk: "Высокий",
      price: mockTenders
        .filter((t) => t.risk === "высокий")
        .reduce((sum, t) => sum + t.price, 0),
    },
  ];

  const chartPriceConfig = {
    price: { label: "Сумма цен тендеров", color: "var(--chart-5)" },
  } satisfies ChartConfig;

  // 3. Количество поставщиков по тендерам
  const chartSuppliersData = mockTenders.map((t) => ({
    title: t.title.length > 10 ? t.title.slice(0, 10) + "..." : t.title,
    suppliers: t.supplierCount,
  }));

  const chartSuppliersConfig = {
    suppliers: { label: "Количество поставщиков", color: "var(--chart-2)" },
  } satisfies ChartConfig;
  const supplierCategories = [
    {
      name: "Мало (<3)",
      value: mockTenders.filter((t) => t.supplierCount < 3).length,
    },
    {
      name: "Средне (3-5)",
      value: mockTenders.filter(
        (t) => t.supplierCount >= 3 && t.supplierCount <= 5
      ).length,
    },
    {
      name: "Много (>5)",
      value: mockTenders.filter((t) => t.supplierCount > 5).length,
    },
  ];
  const supplierColors = [
    "var(--chart-1)",
    "var(--chart-2)",
    "var(--chart-3)",
    "var(--chart-4)",
    "var(--chart-5)",
  ];
  return (
    <div className="flex flex-1 flex-col gap-4 p-4 h-full w-full">
      {/* Верхние карточки */}
      <div className="grid auto-rows-fr gap-4 md:grid-cols-4">
        <Card className="h-full p-4 flex flex-col justify-between">
          <div className="text-sm font-medium text-muted-foreground">
            Всего тендеров
          </div>
          <div className="text-2xl font-bold">{mockTenders.length}</div>
        </Card>
        <Card className="h-full p-4 flex flex-col justify-between">
          <div className="text-sm font-medium text-muted-foreground">
            Средний риск
          </div>
          <div className="text-2xl font-bold">
            {(
              ((riskCounts["высокий"] * 2 + riskCounts["средний"]) /
                (mockTenders.length * 2)) *
              100
            ).toFixed(0)}
            %
          </div>
        </Card>
        <Card className="h-full p-4 flex flex-col justify-between">
          <div className="text-sm font-medium text-muted-foreground">
            Всего поставщиков
          </div>
          <div className="text-2xl font-bold">
            {mockTenders.reduce((sum, t) => sum + t.supplierCount, 0)}
          </div>
        </Card>
        <Card className="h-full p-4 flex flex-col justify-between">
          <div className="text-sm font-medium text-muted-foreground">
            Максимальная цена тендера
          </div>
          <div className="text-2xl font-bold">
            {Math.max(...mockTenders.map((t) => t.price)).toLocaleString()} ₸
          </div>
        </Card>
        <Card className="h-full p-4 flex flex-col justify-between">
          <div className="text-sm font-medium text-muted-foreground">
            Минимальная цена тендера
          </div>
          <div className="text-2xl font-bold">
            {Math.min(...mockTenders.map((t) => t.price)).toLocaleString()} ₸
          </div>
        </Card>
        <Card className="h-full p-4 flex flex-col justify-between">
          <div className="text-sm font-medium text-muted-foreground">
            Средняя цена тендера
          </div>
          <div className="text-2xl font-bold">
            {(
              mockTenders.reduce((sum, t) => sum + t.price, 0) /
              mockTenders.length
            ).toLocaleString()}{" "}
            ₸
          </div>
        </Card>
        <Card className="h-full p-4 flex flex-col justify-between">
          <div className="text-sm font-medium text-muted-foreground">
            Тендеры дороже среднего
          </div>
          <div className="text-2xl font-bold">
            {
              mockTenders.filter(
                (t) =>
                  t.price >
                  mockTenders.reduce((sum, t) => sum + t.price, 0) /
                    mockTenders.length
              ).length
            }
          </div>
        </Card>

        <Card className="h-full p-4 flex flex-col justify-between">
          <div className="text-sm font-medium text-muted-foreground">
            Самый конкурентный тендер
          </div>
          <div className="text-2xl font-bold">
            {
              mockTenders.reduce(
                (max, t) => (t.supplierCount > max.supplierCount ? t : max),
                mockTenders[0]
              ).title
            }
          </div>
        </Card>
      </div>
      <div className="grid auto-rows-fr gap-4 md:grid-cols-3">
        {/* 1. График количества тендеров по риску */}
        <Card className="w-full p-4">
          <h3 className="font-semibold mb-2">Тендеры по риску</h3>
          <ChartContainer
            className="min-h-[250px] w-full"
            config={chartRiskConfig}
          >
            <BarChart accessibilityLayer data={chartRiskData}>
              <CartesianGrid vertical={false} />
              <XAxis dataKey="risk" tickLine={false} axisLine={true} />
              <YAxis tickLine={false} axisLine={true} />
              <Bar dataKey="count" radius={4}>
                {chartRiskData.map((entry) => (
                  <Cell key={entry.risk} fill={riskColors[entry.risk]} />
                ))}
              </Bar>
              <ChartTooltip
                content={
                  <ChartTooltipContent labelKey="count" nameKey="risk" />
                }
              />
              <Legend
                payload={chartRiskData.map((entry) => ({
                  id: entry.risk,
                  value: entry.risk,
                  type: "square",
                  color: riskColors[entry.risk],
                }))}
              />
            </BarChart>
          </ChartContainer>
        </Card>

        {/* 2. График суммы цен по риску */}
        <Card className="w-full p-4">
          <h3 className="font-semibold mb-2">Сумма цен тендеров по риску</h3>
          <ChartContainer
            className="min-h-[250px] w-full"
            config={chartPriceConfig}
          >
            <BarChart accessibilityLayer data={chartPriceData}>
              <CartesianGrid vertical={false} />
              <XAxis dataKey="risk" tickLine={false} axisLine={true} />
              <YAxis tickLine={false} axisLine={true} />

              <Bar dataKey="price" radius={4}>
                {chartPriceData.map((entry) => (
                  <Cell key={entry.risk} fill={riskColors[entry.risk]} />
                ))}
              </Bar>
              <ChartTooltip
                content={
                  <ChartTooltipContent labelKey="price" nameKey="risk" />
                }
              />
              <Legend
                payload={chartPriceData.map((entry) => ({
                  id: entry.risk,
                  value: entry.risk,
                  type: "square",
                  color: riskColors[entry.risk],
                }))}
              />
            </BarChart>
          </ChartContainer>
        </Card>

        {/* 3. График количества поставщиков по тендеру */}
        <Card className="w-full p-4">
          <h3 className="font-semibold mb-2">
            Распределение тендеров по поставщикам
          </h3>
          <ChartContainer
            className="min-h-[250px] w-full"
            config={{ value: { label: "Количество тендеров" } } as ChartConfig}
          >
            <PieChart>
              <Pie
                data={supplierCategories}
                dataKey="value"
                nameKey="name"
                cx="50%"
                cy="50%"
                outerRadius={80}
                label
              >
                {supplierCategories.map((entry, index) => (
                  <Cell
                    key={entry.name}
                    fill={supplierColors[index % supplierColors.length]}
                  />
                ))}
              </Pie>
              <ChartTooltip
                content={
                  <ChartTooltipContent labelKey="value" nameKey="name" />
                }
              />
              <Legend
                layout="vertical"
                verticalAlign="middle"
                align="right"
                payload={supplierCategories.map((entry, index) => ({
                  id: entry.name,
                  value: entry.name,
                  type: "square",
                  color: supplierColors[index % supplierColors.length],
                }))}
              />
            </PieChart>
          </ChartContainer>
        </Card>
      </div>
      <Card className="h-full w-full overflow-auto p-2 gap-3">
        <h3 className="font-semibold text-center">Последние тендеры</h3>
        <TendersTable tenders={topTenders} />
      </Card>
    </div>
  );
}
