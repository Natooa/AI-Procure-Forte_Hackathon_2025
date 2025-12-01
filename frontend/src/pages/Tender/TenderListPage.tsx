import { useState } from "react";
import { Card } from "@/components/ui/card";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Pagination,
  PaginationContent,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
  PaginationEllipsis,
} from "@/components/ui/pagination";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { mockTenders } from "./mockTenders";
import { TendersTable } from "./TendersTable";
import { SortAscIcon, SortDescIcon } from "lucide-react";

export default function TenderListPage() {
  const [search, setSearch] = useState("");
  const [riskFilter, setRiskFilter] = useState("all");
  const [affiliatedFilter, setAffiliatedFilter] = useState("all");
  const [sortOption, setSortOption] = useState("none");
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);

  const filteredTenders = mockTenders
    .filter((t) => t.title.toLowerCase().includes(search.toLowerCase()))
    .filter((t) => (riskFilter !== "all" ? t.risk === riskFilter : true))
    .filter((t) =>
      affiliatedFilter === "affiliated"
        ? t.affiliated
        : affiliatedFilter === "notAffiliated"
        ? !t.affiliated
        : true
    )
    .sort((a, b) => {
      switch (sortOption) {
        case "priceAsc":
          return a.price - b.price;
        case "priceDesc":
          return b.price - a.price;
        case "deadlineAsc":
          return (
            new Date(a.deadline).getTime() - new Date(b.deadline).getTime()
          );
        case "deadlineDesc":
          return (
            new Date(b.deadline).getTime() - new Date(a.deadline).getTime()
          );
        default:
          return 0;
      }
    });

  const totalPages = Math.ceil(filteredTenders.length / pageSize);
  const paginatedTenders = filteredTenders.slice(
    (currentPage - 1) * pageSize,
    currentPage * pageSize
  );

  const pagesToShow = [];
  for (let i = 1; i <= totalPages; i++) {
    pagesToShow.push(i);
  }

  return (
    <div className="flex flex-col gap-4 p-4">
      {/* Фильтры и поиск */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-4 p-4">
        {/* Поиск */}
        <div className="flex flex-col">
          <label className="text-sm font-medium mb-1">Поиск</label>
          <Input
            type="text"
            placeholder="Поиск по названию тендера"
            value={search}
            className="w-full"
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>

        {/* Фильтр по риску */}
        <div className="flex flex-col">
          <label className="text-sm font-medium mb-1">Риск</label>
          <Select value={riskFilter} onValueChange={setRiskFilter}>
            <SelectTrigger className="w-full">
              <SelectValue placeholder="Выберите риск" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">Все</SelectItem>
              <SelectItem value="низкий">Низкий</SelectItem>
              <SelectItem value="средний">Средний</SelectItem>
              <SelectItem value="высокий">Высокий</SelectItem>
            </SelectContent>
          </Select>
        </div>

        {/* Фильтр по аффилированности */}
        <div className="flex flex-col">
          <label className="text-sm font-medium mb-1">Связанные</label>
          <Select value={affiliatedFilter} onValueChange={setAffiliatedFilter}>
            <SelectTrigger className="w-full">
              <SelectValue placeholder="Выберите" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">Все</SelectItem>
              <SelectItem value="affiliated">Связанные</SelectItem>
              <SelectItem value="notAffiliated">Не связанные</SelectItem>
            </SelectContent>
          </Select>
        </div>

        {/* Сортировка */}
        <div className="flex flex-col">
          <label className="text-sm font-medium mb-1">Сортировка</label>
          <Select value={sortOption} onValueChange={setSortOption}>
            <SelectTrigger className="w-full">
              <SelectValue placeholder="Выберите" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="none">Без сортировки</SelectItem>
              <SelectItem value="priceAsc">
                Цена <SortAscIcon />
              </SelectItem>
              <SelectItem value="priceDesc">
                Цена <SortDescIcon />
              </SelectItem>
              <SelectItem value="deadlineAsc">
                Срок <SortAscIcon />
              </SelectItem>
              <SelectItem value="deadlineDesc">
                Срок <SortDescIcon />
              </SelectItem>
            </SelectContent>
          </Select>
        </div>

        {/* Кол-во на странице */}
        <div className="flex flex-col">
          <label className="text-sm font-medium mb-1">На странице</label>
          <Select
            value={pageSize.toString()}
            onValueChange={(v) => {
              setPageSize(Number(v));
              setCurrentPage(1);
            }}
          >
            <SelectTrigger className="w-full">
              <SelectValue placeholder="Выберите" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="5">5</SelectItem>
              <SelectItem value="10">10</SelectItem>
              <SelectItem value="20">20</SelectItem>
              <SelectItem value="50">50</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </div>

      {/* Таблица */}
      <Card className="h-full w-full overflow-auto p-2">
        <TendersTable tenders={paginatedTenders} />
      </Card>

      {/* Пагинация */}
      <Pagination>
        <PaginationContent>
          <PaginationItem>
            <PaginationPrevious
              href="#"
              onClick={(e) => {
                e.preventDefault();
                setCurrentPage((prev) => Math.max(prev - 1, 1));
              }}
            />
          </PaginationItem>

          {pagesToShow.map((page) => (
            <PaginationItem key={page}>
              {Math.abs(page - currentPage) > 2 &&
              page !== 1 &&
              page !== totalPages ? (
                <PaginationEllipsis />
              ) : (
                <PaginationLink
                  href="#"
                  isActive={page === currentPage}
                  onClick={(e) => {
                    e.preventDefault();
                    setCurrentPage(page);
                  }}
                >
                  {page}
                </PaginationLink>
              )}
            </PaginationItem>
          ))}

          <PaginationItem>
            <PaginationNext
              href="#"
              onClick={(e) => {
                e.preventDefault();
                setCurrentPage((prev) => Math.min(prev + 1, totalPages));
              }}
            />
          </PaginationItem>
        </PaginationContent>
      </Pagination>
    </div>
  );
}
