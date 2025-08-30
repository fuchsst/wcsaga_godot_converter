#!/usr/bin/env python3
import logging
from typing import Any, BinaryIO, Dict, List

# Import unified binary reader
from .pof_binary_reader import create_reader

# Import Vector3D if needed for type hinting or direct use
# from .pof_types import Vector3D

logger = logging.getLogger(__name__)


def read_insg_chunk(f: BinaryIO, length: int) -> List[Dict[str, Any]]:
    """Parses the Insignia (INSG) chunk."""
    reader = create_reader(f)
    logger.debug("Reading INSG chunk...")
    num_insignia = reader.read_int32()
    insignias = []
    for _ in range(num_insignia):
        ins_data = {"faces": []}
        ins_data["lod"] = reader.read_int32()
        num_faces = reader.read_int32()
        num_verts = reader.read_int32()  # Total verts for this insignia's geometry
        verts = [
            reader.read_vector3d() for _ in range(num_verts)
        ]  # Read Vector3D objects
        ins_data["offset"] = reader.read_vector3d().to_list()
        for _ in range(num_faces):
            face_verts_with_uvs = []
            indices = [reader.read_int32() for _ in range(3)]
            uvs = [(reader.read_float32(), reader.read_float32()) for _ in range(3)]
            valid_indices = True
            for k in range(3):
                idx = indices[k]
                if idx < 0 or idx >= num_verts:
                    logger.error(
                        f"Invalid vertex index {idx} in INSG face (max: {num_verts-1}). Skipping face."
                    )
                    valid_indices = False
                    break
                face_verts_with_uvs.append(
                    {"position": verts[idx].to_list(), "u": uvs[k][0], "v": uvs[k][1]}
                )
            if valid_indices:
                ins_data["faces"].append({"vertices": face_verts_with_uvs})
        insignias.append(ins_data)
    return insignias
