import { useParams, Link, useNavigate } from "react-router-dom";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { mockTenders } from "./mockTenders";
import { ArrowLeft } from "lucide-react";
import { Button } from "@/components/ui/button";

export default function TenderPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const tender = mockTenders.find((t) => t.id === id);

  if (!tender) {
    return <div className="p-4 text-lg font-medium">Тендер не найден</div>;
  }

  return (
    <div className="p-4 max-w-4xl mx-auto space-y-6">
      {/* Back button */}
      <Button
        variant={"outline"}
        onClick={() => navigate(-1)}
        className="flex items-center gap-2 text-sm hover:underline w-fit"
      >
        <ArrowLeft size={16} />
        Назад
      </Button>

      {/* Title */}
      <h1 className="text-3xl font-bold">{tender.title}</h1>

      {/* Main info */}
      <Card>
        <CardHeader>
          <CardTitle>Информация о тендере</CardTitle>
        </CardHeader>
        <CardContent className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <p className="text-sm text-muted-foreground">ID тендера</p>
            <p className="font-medium">{tender.id}</p>
          </div>

          <div>
            <p className="text-sm text-muted-foreground">Цена</p>
            <p className="font-medium">{tender.price.toLocaleString()} ₸</p>
          </div>

          <div>
            <p className="text-sm text-muted-foreground">Дедлайн</p>
            <p className="font-medium">{tender.deadline}</p>
          </div>

          <div>
            <p className="text-sm text-muted-foreground">
              Количество поставщиков
            </p>
            <p className="font-medium">{tender.supplierCount}</p>
          </div>

          <div>
            <p className="text-sm text-muted-foreground">Заказчик</p>
            <p className="font-medium">{tender.customer}</p>
          </div>

          <div>
            <p className="text-sm text-muted-foreground">Риск</p>
            <Badge
              variant={
                tender.risk === "высокий"
                  ? "destructive"
                  : tender.risk === "средний"
                  ? "secondary"
                  : "default"
              }
            >
              {tender.risk}
            </Badge>
          </div>

          <div>
            <p className="text-sm text-muted-foreground">Аффилированность</p>
            <Badge variant={tender.affiliated ? "destructive" : "outline"}>
              {tender.affiliated ? "Аффилирован" : "Не аффилирован"}
            </Badge>
          </div>
        </CardContent>
      </Card>

      {/* Additional details or future block */}
      <Card>
        <CardHeader>
          <CardTitle>Детали</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground">
            Здесь можно разместить: описание закупки, документы, участников,
            историю изменений, риск-анализ и т.п.
          </p>
        </CardContent>
      </Card>
    </div>
  );
}
