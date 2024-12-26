# Program Kasir Sederhana

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
from rich.style import Style
from rich import box
from datetime import datetime

console = Console()

def tampilkan_header():
    title = Text("PROGRAM KASIR SEDERHANA", style="bold white on blue")
    subtitle = Text(f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", style="italic")
    console.print(Panel(title, subtitle=subtitle, box=box.DOUBLE, border_style="blue"))

def tampilkan_menu(daftar_menu):
    table = Table(title="DAFTAR MENU", box=box.ROUNDED, border_style="cyan", title_style="bold cyan")
    table.add_column("No", style="cyan", justify="center")
    table.add_column("Nama Menu", style="white")
    table.add_column("Harga", justify="right", style="green")

    for idx, (menu, harga) in enumerate(daftar_menu.items(), 1):
        table.add_row(
            str(idx),
            menu.title(),
            f"Rp {harga:,}"
        )
    
    console.print(table)

def tampilkan_struk(keranjang, daftar_menu):
    table = Table(title="STRUK PEMBELIAN", box=box.DOUBLE_EDGE, border_style="yellow", title_style="bold yellow")
    table.add_column("Menu", style="white")
    table.add_column("Qty", justify="center", style="cyan")
    table.add_column("Harga Satuan", justify="right", style="green")
    table.add_column("Subtotal", justify="right", style="green")
    
    total = 0
    menu_count = {}
    
    for menu in keranjang:
        menu_count[menu] = menu_count.get(menu, 0) + 1
    
    for menu, qty in menu_count.items():
        harga = daftar_menu[menu]
        subtotal = harga * qty
        total += subtotal
        table.add_row(
            menu.title(),
            str(qty),
            f"Rp {harga:,}",
            f"Rp {subtotal:,}"
        )
    
    console.print(table)
    console.print(Panel(f"Total Pembayaran: Rp {total:,}", 
                       style="bold green",
                       border_style="green"))
    return total

def tampilkan_keranjang(keranjang):
    if not keranjang:
        console.print("[yellow]Keranjang kosong![/yellow]")
        return

    table = Table(title="ISI KERANJANG", box=box.ROUNDED, border_style="magenta", title_style="bold magenta")
    table.add_column("No", style="magenta", justify="center")
    table.add_column("Menu", style="white")
    table.add_column("Jumlah", justify="center", style="cyan")

    menu_count = {}
    for menu in keranjang:
        menu_count[menu] = menu_count.get(menu, 0) + 1

    for idx, (menu, qty) in enumerate(menu_count.items(), 1):
        table.add_row(str(idx), menu.title(), str(qty))
    
    console.print(table)

def tampilkan_menu_pilihan():
    menu_style = Style(color="cyan")
    console.print("\n[bold cyan]MENU PILIHAN:[/bold cyan]")
    options = [
        "1. Tambah pesanan",
        "2. Lihat keranjang",
        "3. Selesai dan bayar",
        "4. Keluar"
    ]
    for option in options:
        console.print(f"  {option}", style=menu_style)

def main():
    daftar_menu = {
        "Nasi Goreng": 25000,
        "Nasi Kuning": 10000,
        "Teh Manis": 5000,
        "STMJ": 19000,
        "Mie Goreng": 20000,
        "Es Jeruk": 7000
    }
    
    keranjang = []
    
    tampilkan_header()
    tampilkan_menu(daftar_menu)
    
    while True:
        tampilkan_menu_pilihan()
        pilihan = Prompt.ask("\nMasukkan pilihan", choices=["1", "2", "3", "4"])
        
        if pilihan == "1":
            while True:
                console.print("\n[cyan]Menu yang tersedia:[/cyan]")
                tampilkan_menu(daftar_menu)
                pesanan = Prompt.ask("\nMasukkan nama menu (ketik 'selesai' untuk kembali)").title()
                
                if pesanan.lower() == 'selesai':
                    break
                if pesanan in daftar_menu:
                    keranjang.append(pesanan)
                    console.print(f"[green]✓ {pesanan} ditambahkan ke keranjang![/green]")
                else:
                    console.print("[red]✗ Menu tidak tersedia![/red]")
        
        elif pilihan == "2":
            tampilkan_keranjang(keranjang)
        
        elif pilihan == "3":
            if keranjang:
                total = tampilkan_struk(keranjang, daftar_menu)
                while True:
                    try:
                        uang = float(Prompt.ask("\nMasukkan jumlah uang", default="0"))
                        if uang >= total:
                            kembalian = uang - total
                            console.print(Panel(f"Kembalian: Rp {kembalian:,}", 
                                             style="bold green",
                                             border_style="green"))
                            console.print("[bold green]Terima kasih telah berbelanja! 🙏[/bold green]")
                            return
                        else:
                            console.print("[red]Uang tidak cukup![/red]")
                    except ValueError:
                        console.print("[red]Masukkan nominal yang valid![/red]")
            else:
                console.print("[yellow]Keranjang kosong! Tidak dapat melakukan pembayaran.[/yellow]")
        
        elif pilihan == "4":
            console.print(Panel.fit("Terima kasih telah menggunakan program ini! 👋", 
                                  style="bold blue",
                                  border_style="blue"))
            break

if __name__ == "__main__":
    main()
