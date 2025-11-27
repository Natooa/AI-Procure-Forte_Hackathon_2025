import { Link } from "react-router-dom";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { getRiskClasses } from "@/utils/getRiskClasses";
import type { Tender } from "./mockTenders";

export function TendersTable({ tenders }: { tenders: Tender[] }) {
  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>ID</TableHead>
          <TableHead>Название</TableHead>
          <TableHead>Цена</TableHead>
          <TableHead>Срок</TableHead>
          <TableHead>Клиент</TableHead>
          <TableHead>Поставщики</TableHead>
          <TableHead>Риск</TableHead>
          <TableHead>Детали</TableHead>
        </TableRow>
      </TableHeader>

      <TableBody>
        {tenders.map((t) => (
          <TableRow key={t.id}>
            <TableCell className="font-medium">{t.id}</TableCell>
            <TableCell>{t.title}</TableCell>
            <TableCell>{t.price.toLocaleString()} ₸</TableCell>
            <TableCell>{t.deadline}</TableCell>
            <TableCell>{t.customer}</TableCell>
            <TableCell>{t.supplierCount}</TableCell>

            <TableCell>
              <span
                className={`px-2 py-1 rounded-full text-xs font-bold ${getRiskClasses(
                  t.risk
                )}`}
              >
                {t.risk.toUpperCase()}
              </span>
            </TableCell>

            <TableCell>
              <Link
                to={`/tender/${t.id}`}
                className="hover:underline font-medium"
              >
                Открыть
              </Link>
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
}
