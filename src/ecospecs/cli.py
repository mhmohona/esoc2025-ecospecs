import os 
import typer
from pathlib import Path
from typing import List, Optional
from .parsing.table_processor import process_file
from .utils.file_io import save_tables

app = typer.Typer()

@app.command()
def parse(
    file_path: Path,
    output_dir: str = typer.Option(
        "output",
        "--output",
        "-o",
        help="Output directory path"
    )
):
    """Parse tables from document and save as .docx"""
    try:
        tables = process_file(file_path)

        output_path = Path(output_dir) / f"{file_path.stem}_parsed.docx"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        save_tables(tables, output_path, "docx")
        typer.secho(f"✅ Saved {len(tables)} tables to {output_path}", fg="green")
        
        # Display results in console
        # typer.echo(f"\nFound {len(tables)} tables in {file_path}")
        # for i, table in enumerate(tables, 1):
        #     typer.echo(f"\nTable {i}:")
        #     for row in table:
        #         typer.echo(" | ".join(row))
                
    except Exception as e:
        typer.secho(f"❌ Error: {str(e)}", fg="red")

# cli.py
@app.command()
def generate(
    prompt: str,
    headers: List[str],
    output_file: Optional[Path] = typer.Option(
        None,
        "--output",
        "-o",
        help="Output file path (.docx)"
    )
):
    """Generate tables using OSS models"""
    try:
        typer.secho("🔮 Generating table...", fg="blue")
        typer.echo(f"📝 Prompt: {prompt}")
        typer.echo(f"🏷️ Headers: {headers}")

        from ecospecs.genai.table_generator import generate_table
        generated_table = generate_table(prompt, headers)

        if output_file:
            output_file = output_file.with_suffix(".docx")
            save_tables([generated_table], output_file, "docx")
            typer.secho(f"✅ Saved generated table to {output_file}", fg="green")
        else:
            typer.echo("\nGenerated Table:")
            for row in generated_table:
                typer.echo(" | ".join(row))
                
    except Exception as e:
        typer.secho(f"❌ Error: {str(e)}", fg="red")
        
if __name__ == "__main__":
    app()
