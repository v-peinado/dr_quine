#!/usr/bin/env python3
"""
Verificador de Quine para colleen.c
Ejecuta múltiples pruebas para verificar que el quine funciona correctamente.
"""

import subprocess
import hashlib
import difflib
import os
import sys

def print_header(text):
    """Imprime un encabezado formateado"""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}")

def compile_program(source_file, output_file="colleen"):
    """Compila el programa C"""
    print_header("COMPILANDO PROGRAMA")
    try:
        result = subprocess.run(
            ["gcc", "-Wall", "-Wextra", "-Werror", "-o", output_file, source_file],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            print(f"✅ Compilación exitosa: {source_file} -> {output_file}")
            return True
        else:
            print(f"❌ Error de compilación:")
            print(result.stderr)
            return False
    except FileNotFoundError:
        print("❌ Error: gcc no encontrado. Asegúrate de tenerlo instalado.")
        return False

def run_program(executable="./colleen"):
    """Ejecuta el programa y captura su salida"""
    print_header("EJECUTANDO PROGRAMA")
    try:
        result = subprocess.run([executable], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Programa ejecutado exitosamente")
            return result.stdout
        else:
            print(f"❌ Error al ejecutar el programa:")
            print(result.stderr)
            return None
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el ejecutable {executable}")
        return None

def read_file(filename):
    """Lee el contenido de un archivo"""
    try:
        with open(filename, 'r') as f:
            return f.read()
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo {filename}")
        return None

def test_diff(original, output):
    """Prueba usando diff (comparación línea por línea)"""
    print_header("PRUEBA: DIFF")
    
    if original == output:
        print("✅ Los archivos son idénticos")
        return True
    else:
        print("❌ Se encontraron diferencias:")
        diff = difflib.unified_diff(
            original.splitlines(keepends=True),
            output.splitlines(keepends=True),
            fromfile='colleen.c (original)',
            tofile='salida (output)',
            lineterm=''
        )
        for line in diff:
            print(line)
        return False

def test_byte_comparison(original, output):
    """Prueba comparación byte a byte"""
    print_header("PRUEBA: COMPARACIÓN BYTE A BYTE")
    
    if len(original) != len(output):
        print(f"❌ Los archivos tienen diferente tamaño:")
        print(f"   Original: {len(original)} bytes")
        print(f"   Salida:   {len(output)} bytes")
        print(f"   Diferencia: {abs(len(original) - len(output))} bytes")
        return False
    
    for i, (a, b) in enumerate(zip(original, output)):
        if a != b:
            print(f"❌ Primera diferencia en byte {i}:")
            print(f"   Original: {repr(a)} (ASCII: {ord(a)})")
            print(f"   Salida:   {repr(b)} (ASCII: {ord(b)})")
            return False
    
    print("✅ Todos los bytes son idénticos")
    return True

def test_checksum(original, output):
    """Prueba usando checksums (MD5 y SHA256)"""
    print_header("PRUEBA: CHECKSUMS")
    
    md5_original = hashlib.md5(original.encode()).hexdigest()
    md5_output = hashlib.md5(output.encode()).hexdigest()
    
    sha256_original = hashlib.sha256(original.encode()).hexdigest()
    sha256_output = hashlib.sha256(output.encode()).hexdigest()
    
    print(f"MD5 Original: {md5_original}")
    print(f"MD5 Salida:   {md5_output}")
    
    if md5_original == md5_output:
        print("✅ MD5 checksums coinciden")
    else:
        print("❌ MD5 checksums difieren")
    
    print(f"\nSHA256 Original: {sha256_original}")
    print(f"SHA256 Salida:   {sha256_output}")
    
    if sha256_original == sha256_output:
        print("✅ SHA256 checksums coinciden")
    else:
        print("❌ SHA256 checksums difieren")
    
    return md5_original == md5_output and sha256_original == sha256_output

def test_line_endings(original, output):
    """Verifica los finales de línea y caracteres finales"""
    print_header("PRUEBA: CARACTERES FINALES")
    
    # Mostrar últimos 20 caracteres
    print("Últimos 20 caracteres del original:")
    for i, char in enumerate(original[-20:]):
        if char == '\n':
            print(f"  Pos {i}: '\\n' (salto de línea)")
        elif char == '\t':
            print(f"  Pos {i}: '\\t' (tabulador)")
        elif char == ' ':
            print(f"  Pos {i}: ' ' (espacio)")
        else:
            print(f"  Pos {i}: '{char}'")
    
    print("\nÚltimos 20 caracteres de la salida:")
    for i, char in enumerate(output[-20:]):
        if char == '\n':
            print(f"  Pos {i}: '\\n' (salto de línea)")
        elif char == '\t':
            print(f"  Pos {i}: '\\t' (tabulador)")
        elif char == ' ':
            print(f"  Pos {i}: ' ' (espacio)")
        else:
            print(f"  Pos {i}: '{char}'")
    
    # Verificar si hay salto de línea al final
    original_ends_newline = original.endswith('\n')
    output_ends_newline = output.endswith('\n')
    
    print(f"\n¿Original termina con salto de línea? {'Sí' if original_ends_newline else 'No'}")
    print(f"¿Salida termina con salto de línea? {'Sí' if output_ends_newline else 'No'}")
    
    if original_ends_newline != output_ends_newline:
        print("❌ Los finales de archivo no coinciden")
        return False
    else:
        print("✅ Los finales de archivo coinciden")
        return True

def test_recompilation(output_content):
    """Prueba que la salida se pueda compilar y ejecutar igual"""
    print_header("PRUEBA: RECOMPILACIÓN")
    
    # Guardar la salida en un archivo temporal
    with open("colleen_output.c", "w") as f:
        f.write(output_content)
    
    # Compilar la salida
    if not compile_program("colleen_output.c", "colleen_output"):
        print("❌ La salida no se pudo compilar")
        return False
    
    # Ejecutar la salida compilada
    second_output = run_program("./colleen_output")
    if second_output is None:
        print("❌ La salida compilada no se pudo ejecutar")
        return False
    
    # Comparar la segunda salida con la primera
    if output_content == second_output:
        print("✅ La salida genera el mismo código cuando se ejecuta")
        return True
    else:
        print("❌ La salida genera código diferente cuando se ejecuta")
        return False

def main():
    print("🔍 VERIFICADOR DE QUINE PARA colleen.c")
    print("="*60)
    
    # Verificar que el archivo existe
    if not os.path.exists("colleen.c"):
        print("❌ Error: No se encontró el archivo colleen.c")
        sys.exit(1)
    
    # Compilar el programa
    if not compile_program("colleen.c"):
        sys.exit(1)
    
    # Ejecutar el programa
    output = run_program()
    if output is None:
        sys.exit(1)
    
    # Leer el archivo original
    original = read_file("colleen.c")
    if original is None:
        sys.exit(1)
    
    # Ejecutar todas las pruebas
    results = []
    results.append(("Diff", test_diff(original, output)))
    results.append(("Comparación byte a byte", test_byte_comparison(original, output)))
    results.append(("Checksums", test_checksum(original, output)))
    results.append(("Caracteres finales", test_line_endings(original, output)))
    results.append(("Recompilación", test_recompilation(output)))
    
    # Resumen final
    print_header("RESUMEN DE RESULTADOS")
    all_passed = True
    for test_name, passed in results:
        status = "✅ PASÓ" if passed else "❌ FALLÓ"
        print(f"{test_name}: {status}")
        if not passed:
            all_passed = False
    
    print("\n" + "="*60)
    if all_passed:
        print("🎉 ¡FELICITACIONES! Tu quine funciona perfectamente 🎉")
    else:
        print("❌ Tu quine necesita ajustes. Revisa los errores arriba.")
    print("="*60)
    
    # Limpiar archivos temporales
    if os.path.exists("colleen_output.c"):
        os.remove("colleen_output.c")
    if os.path.exists("colleen_output"):
        os.remove("colleen_output")

if __name__ == "__main__":
    main()