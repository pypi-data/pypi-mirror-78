import subprocess
import json
import glob
import shutil
import uuid
import datetime
from pathlib import Path

from typing import List, Optional

import typer

app = typer.Typer()

@app.callback()
def callback():
    """
    glb(web images) -> glb(basis images)

    A CLI to convert gltf/glb assets with png/jpg textures into glb
    assets with embedded basis/ktx2 textures.

    Made with typer -> [check it](https://github.com/tiangolo/typer)

    """
def compress_images(
    materials: dict,
    images: dict, 
    gltf_folder: Path,
    basisu_flags: List[str],
    verbose: int
):
    linear_indices = list()
    for material in materials:
        linear_indices.append(material["normalTexture"]["index"])
        linear_indices.append(material["pbrMetallicRoughness"]["metallicRoughnessTexture"]["index"])

    index_counter = 0
    with typer.progressbar(images,label="Compressing") as images:
        for image in images:
            if image["mimeType"] not in ["image/png","image/jpg"]:
                continue
            compress_command = [
                "basisu", 
                "-file", str(gltf_folder / image["uri"]), 
                "-output_path", str(gltf_folder)
            ]
            if index_counter in linear_indices:
                compress_command.append("-linear")
            compress_command+=basisu_flags
            if verbose>0:
                command_str = ' '.join(compress_command)
                typer.echo(f"\n{command_str}")
            index_counter += 1
            compress_result = subprocess.run(compress_command,capture_output=(verbose<=1))
            if compress_result.returncode!=0:
                typer.secho(f"unable to compress {image}",fg=typer.colors.RED)
            else:
                image["uri"] = str(Path(image["uri"]).with_suffix(".basis"))

def write_new_gltf(
    gltf_dict: dict, 
    new_gltf_file_path: str,
    verbose: int
):
    if(verbose>0):
        typer.echo("writing new gltf") 
    new_gltf_json = json.dumps(gltf_dict)
    f = open(new_gltf_file_path, "w")
    f.write(new_gltf_json)
    f.close() 
    if(verbose>0):
        typer.echo("writing new gltf done")  

def gltf_pipeline_command(
    file_input: Path,
    file_output: Path,
    flags: List[Optional[str]],
    verbose: int
):
    gltf_command = [
        "gltf-pipeline", 
        "-i", str(file_input), 
        "-o", str(file_output),
    ]
    gltf_command += flags

    if verbose>0:
        command_str = ' '.join(gltf_command)
        typer.echo(f"\n{command_str}")
    gltf_command_result = subprocess.run(gltf_command,capture_output=(verbose<=1))
    if gltf_command_result.returncode!=0:
        typer.secho("subprocess returned a non-zero exit code",fg=typer.colors.RED)

@app.command()
def expand_glb(
    input_file: Path = typer.Argument(...,metavar="FILE"),
    verbose: int = typer.Option(0, "--verbose", "-v", count=True),
):
    """
    Expand a glb
    """
    if not input_file.exists():
        typer.secho("input file doesn't exist",fg=typer.colors.RED)
        raise typer.Abort()
    
    suffix = input_file.suffix
    if suffix == ".glb":
        typer.echo(f"expanding {input_file} file") 
        gltf_folder = input_file.with_name(uuid.uuid4().hex[:7]+".gltf")
        gltf_folder.mkdir(exist_ok=True)
        new_gltf_file_path = gltf_folder / "asset.gltf"

        gltf_pipeline_command(
            input_file,
            new_gltf_file_path,
            ["--separateTextures"],
            verbose
        )
    else:
        typer.echo("input file is not a glb")
        raise typer.Abort()

def handle_gltf(
    input_file: Path,
    gltf_folder: Path,
    new_gltf_file_path: Path,
    new_glb_name_path: Path,
    basisu_flags: List[Path],
    tag:str,
    keep_temp_gltf: bool,
    verbose: int
):
    
    gltf_dict = json.loads(new_gltf_file_path.read_text())   

    compress_images(
        gltf_dict["materials"],
        gltf_dict["images"],
        gltf_folder,
        basisu_flags,
        verbose
    )

    write_new_gltf(gltf_dict,new_gltf_file_path,verbose)
    
    gltf_pipeline_command(
        new_gltf_file_path,
        new_glb_name_path,
        [],
        verbose
    )

    if not keep_temp_gltf:
        shutil.rmtree(str(gltf_folder))

@app.command()
def convert(
    input_files: List[Path] = typer.Argument(...,metavar="INPUT"),
    tag: str = typer.Option("basisu",metavar="TAG",show_default=True),
    keep_temp_gltf: bool = typer.Option(False, "--keep-temp-gltf"),
    verbose: int = typer.Option(0, "--verbose", "-v", count=True),
    basisu_flags: List[str] = typer.Option(None, "--basisu-flags", "-bf"),
):
    """
    Convert a glb/gltf (web images) -> glb(basis images)
    """
    for input_file in input_files:
        if not input_file.exists():
            typer.secho(f"input file {input_file} doesn't exist",fg=typer.colors.RED)
            continue
            
        typer.echo(f"processing {input_file}")
        start_time = datetime.datetime.now()

        suffix = input_file.suffix

        if suffix == ".glb":
            gltf_folder = input_file.with_name(uuid.uuid4().hex[:7]+".gltf")
            new_gltf_file_path = gltf_folder / "asset.gltf"   
            new_glb_name = input_file.name[:input_file.name.index(suffix)]+"-"+tag+suffix
            new_glb_name_path = input_file.with_name(new_glb_name)

            gltf_folder.mkdir(exist_ok=True)
            
            gltf_pipeline_command(
                input_file,
                new_gltf_file_path,
                ["--separateTextures"],
                verbose
            )

            handle_gltf(
                input_file,
                gltf_folder,
                new_gltf_file_path,
                new_glb_name_path,
                basisu_flags,
                tag,
                keep_temp_gltf,
                verbose
            )
            

        elif suffix == ".gltf":    
            gltf_folder = input_file.parent.with_name(uuid.uuid4().hex[:7]+".gltf")  
            new_gltf_file_path = gltf_folder / input_file.name
            new_glb_name = input_file.parent.name[:input_file.parent.name.index(suffix)]+"-"+tag+".glb"
            new_glb_name_path = input_file.parent.with_name(new_glb_name)
            
            shutil.copytree(input_file.parent,gltf_folder)

            handle_gltf(
                input_file,
                gltf_folder,
                new_gltf_file_path,
                new_glb_name_path,
                basisu_flags,
                tag,
                keep_temp_gltf,
                verbose
            )

        else:
            typer.echo(f"input file {input_file} is neither glb or gltf")

        total_time = datetime.datetime.now() - start_time
        total_time = str(total_time)[:7]
        typer.echo(f"total process time - {total_time}\n")

if __name__ == "__main__":
    app()