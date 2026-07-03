'use client';

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import { formatCurrency, formatDate } from '@/utils/format';
import { Transaction } from '@/types';

interface PreviewTableProps {
  transactions: Transaction[];
  maxRows?: number;
}

export function PreviewTable({ transactions, maxRows = 10 }: PreviewTableProps) {
  const rows = transactions.slice(0, maxRows);

  if (!rows.length) {
    return <p className="py-8 text-center text-sm text-muted-foreground">No transactions to preview</p>;
  }

  return (
    <div className="rounded-xl border border-border overflow-hidden">
      <div className="max-h-[400px] overflow-auto scrollbar-thin">
        <Table>
          <TableHeader>
            <TableRow className="border-border bg-muted/30 hover:bg-muted/30">
              <TableHead className="text-xs">Date</TableHead>
              <TableHead className="text-xs">Description</TableHead>
              <TableHead className="text-xs">Merchant</TableHead>
              <TableHead className="text-xs">Category</TableHead>
              <TableHead className="text-xs text-right">Amount</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {rows.map((tx, i) => (
              <TableRow key={i} className="border-border">
                <TableCell className="text-xs text-muted-foreground">{formatDate(tx.date)}</TableCell>
                <TableCell className="text-sm">{tx.description}</TableCell>
                <TableCell className="text-sm text-muted-foreground">{tx.merchant}</TableCell>
                <TableCell className="text-sm">
                  <span className="rounded-md bg-muted/50 px-2 py-0.5 text-xs">{tx.category}</span>
                </TableCell>
                <TableCell className={`text-right text-sm font-semibold ${tx.type === 'income' ? 'text-success' : 'text-destructive'}`}>
                  {tx.type === 'income' ? '+' : '-'}{formatCurrency(Math.abs(tx.amount))}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
      {transactions.length > maxRows && (
        <div className="border-t border-border bg-muted/20 px-4 py-2 text-center text-xs text-muted-foreground">
          Showing {maxRows} of {transactions.length} transactions
        </div>
      )}
    </div>
  );
}
