

# **A Technical Framework for Migrating Wing Commander Saga Assets to the Godot Engine**

## **Section 1: Deconstruction of the Freespace 2 Open Asset Pipeline**

The successful migration of game assets from a legacy engine to a modern one requires a foundational, deeply technical understanding of the source data structures. *Wing Commander Saga* (WCS), as a total conversion for the Freespace 2 Open (FS2O) engine, inherits a complex and distributed asset pipeline developed by Volition, Inc..1 A superficial analysis might conclude that a model asset is a single mesh file. However, a thorough deconstruction reveals that a functional game entity—such as a starfighter or capital ship—is a composite asset, a collection of interconnected files that collectively define its geometry, appearance, physics, and gameplay logic. This section provides an exhaustive analysis of these constituent file formats, establishing a complete data model that is essential for architecting a robust conversion tool.

### **1.1 The Anatomy of a Complete Model Asset: Beyond the Mesh**

In the FS2O engine, game data is not stored as loose files but is consolidated into proprietary archive files with a .vp (Volition Package) extension.3 These archives are the primary containers for all game assets, including 3D models, textures, mission files, interface animations, and the critical tabular data files that govern game logic.5 The modding community has developed tools like  
VPView and VP Mage specifically to explore, extract, and repack these archives, which are indispensable for any asset analysis or modification effort.5  
The central challenge in converting WCS assets lies in recognizing and reassembling the "composite asset." A starship, for example, is not defined by a single file. Its existence in the game engine is the result of a runtime synthesis of data from multiple sources. Consider a fighter like the Scimitar:

1. Its 3D geometry, hierarchy of sub-objects (like debris pieces), and the locations of its hardpoints and thrusters are defined in a binary model file, scimitar.pof.4  
2. Its visual appearance is determined by a set of texture files (e.g., scimitar.dds, scimitar-glow.dds) that are referenced by name within the .pof file.10  
3. Its gameplay characteristics—mass, moment of inertia, shield strength, and crucially, which specific weapons it is permitted to mount on its hardpoints—are defined in a plain-text database file named ships.tbl.11  
4. The performance characteristics of the weapons it can carry (e.g., laser damage, missile speed) are, in turn, defined in a separate database file, weapons.tbl.5

This distributed data model means that the game engine performs a "hydration" process at runtime: it loads the geometric shell from the .pof file and then uses the model's name as a key to look up its gameplay properties in the .tbl files. Consequently, any conversion tool that only processes .pof files will produce a visually accurate but functionally inert asset. It will lack physics properties, weapon compatibility information, and other metadata essential for integration into a new game engine. A successful conversion pipeline must be architected as a data integration system, capable of parsing and correlating information from all these disparate file types to reconstruct a complete, self-contained asset definition.

### **1.2 The .POF Model Format: A Deep Dive**

The .POF (Polygon Object File) format is the cornerstone of the FS2O engine's 3D representation. It is a proprietary binary format with a complex structure designed for the rendering and physics capabilities of mid-1990s hardware.

#### **1.2.1 Introduction and Disambiguation**

It is critical to first establish that the Freespace .POF format is entirely unrelated to the similarly named Programmer Object File format used by Intel (formerly Altera) for programming Field-Programmable Gate Arrays (FPGAs).14 This is a frequent point of confusion that can lead to misdirected research. The FS2O  
.POF format originated with Parallax Software, the creators of the *Descent* series, and was subsequently evolved by Volition for the *Freespace* franchise.9 The format specification has been reverse-engineered and documented by the FS2O modding community, providing a clear blueprint for parsing.9

#### **1.2.2 Binary Structure**

The .POF file is a chunk-based binary format using little-endian byte order. The file begins with a simple header, followed by a sequence of data chunks.

* **Header:** The file header consists of an 8-byte sequence:  
  * char file\_id: A magic number signature, which must be 'PSPO' (likely standing for Parallax Software Polygon Object).9  
  * int version: An integer representing the file version. The version is encoded as Major \* 100 \+ Minor. *Descent: Freespace* (FS1) models typically use version 2014 (20.14), while *Freespace 2* models use 2116 (21.16) or 2117 (21.17). This version number is important, as there are slight structural differences between FS1 and FS2 .pof files that a robust parser must account for.9  
* **Chunk-Based System:** Following the header, the file is composed of a series of chunks. Each chunk follows a consistent structure:  
  * char chunk\_id: A four-character ASCII identifier for the chunk type (e.g., 'OHDR', 'OBJ2', 'TXTR').  
  * int length: The size of the chunk's data in bytes. A crucial and non-obvious implementation detail is that this length field *does not* include the 8 bytes of the chunk header itself (chunk\_id \+ length). A parser must therefore advance its file pointer by length \+ 8 bytes to reach the beginning of the next chunk. Failure to account for this is a common source of parsing errors.9

#### **1.2.3 Geometry and Sub-Objects**

The core purpose of the .POF format is to store the model's geometry and hierarchical structure.

* **BSP Tree Representation:** Unlike modern formats that store geometry as simple lists of vertices and indices, the .POF format organizes polygons into a Binary Space Partitioning (BSP) tree. This data structure was used by the original engine to perform efficient visibility culling and collision detection by recursively checking against the planes of the tree.9 For conversion to a modern engine like Godot, this BSP data is largely an artifact. The conversion process must traverse the BSP tree and its associated polygon lists to reconstruct a standard triangle mesh (a flat list of vertex positions, normals, and UV coordinates) that can be used by modern graphics APIs.  
* **Sub-Objects (OBJ2 chunk):** A .POF model is not a monolithic mesh but a hierarchy of "sub-objects." Each sub-object is a distinct collection of polygons, representing a part of the ship like the main hull, a turret, or a piece of debris that breaks off upon destruction. This hierarchy is explicitly defined in the file and must be preserved during conversion, as it maps directly to the node hierarchy concept used in glTF and Godot's scene tree.9 The parent-child relationships between sub-objects are critical for animations and logical grouping.  
* **Levels of Detail (LODs):** The .POF format supports multiple levels of detail. These are not generated algorithmically but are stored as distinct, artist-created sub-objects within the file. For example, a sub-object might be designated as detail0 (the highest quality), while another is detail1, and so on.9 A comprehensive conversion pipeline must identify these LOD sub-objects and export them in a way that Godot's LOD management systems can utilize, rather than treating them as unrelated meshes.

#### **1.2.4 Critical Metadata Points**

Perhaps the most important feature of the .POF format for gameplay purposes is its ability to store a wide variety of named 3D coordinate points and volumes. These are not just visual elements; they are the hooks that connect the 3D model to the game's logic systems. A successful conversion is contingent on extracting and preserving this metadata with high fidelity. The primary tools for editing this data are the POF Construction Suite 2 (PCS2) and ModelView.11

* **Gun & Missile Banks (GPNT, MPNT):** These chunks define the locations and firing vectors for all primary and secondary weapon hardpoints. Each point is a 3D coordinate and a normal vector indicating the direction of fire.11  
* **Docking Points (DOCK):** Defines specific points on the model used for ship-to-ship or ship-to-station docking maneuvers.11  
* **Engine Thrusters (GLOW):** These are points that specify the location and radius for engine glow particle effects. They are distinct from emissive textures.11  
* **Subsystems (SUBS):** This chunk defines named bounding volumes (spheres or boxes) for targetable ship components like engines, turrets, communication arrays, or sensors. These are fundamental to the combat system, allowing players to disable specific parts of an enemy vessel.11  
* **Eyepoint (EYE):** A single point that defines the default camera position for the cockpit view when flying the ship.11  
* **Paths (PATH):** Defines predefined movement paths for other sub-objects, most commonly used to constrain the movement of turrets.11

### **1.3 Texture and Material Representation**

The FS2O engine uses a pre-PBR (Physically Based Rendering) material system. Materials are not defined in a discrete file but are assembled at runtime based on the textures assigned to a model and a strict file naming convention.

* **Texture Formats:** The engine supports several texture formats. Legacy assets from the original *Freespace 2* often use 256-color .PCX files. However, the modern FS2O engine, and thus WCS, primarily relies on the .DDS (DirectDraw Surface) format for its significant advantages in memory usage and performance, as DXT-compressed textures can be decoded directly by the GPU hardware.10 The converter must be able to handle at least  
  .DDS and .PCX, with .DDS being the priority. The most common compression formats are DXT1 (for textures without an alpha channel) and DXT5 (for textures with an alpha channel).10 Support for uncompressed  
  .TGA files is also present in the engine but is less common.10  
* **Non-PBR Map Naming Conventions:** The relationship between different texture maps is not defined within the .pof file or a separate material file. Instead, the engine discovers associated maps by searching the filesystem for files that share a base name with the primary texture but have specific suffixes. This file-system-aware discovery process is a non-obvious but essential behavior that the conversion tool must replicate.10  
  * TextureName.dds: This is the **base color map** (also known as the diffuse map). Its filename is what is stored in the .pof file's texture chunk.  
  * TextureName-glow.dds: This is an **emissive map**. It is an additive texture used for effects like glowing cockpit windows, running lights, or engine nacelles. It does not use an alpha channel, so DXT1 is the recommended format.10  
  * TextureName-shine.dds: This is a **specular map**. The RGB channels control the color and intensity of specular highlights. A crucial detail for conversion is that the *alpha channel* of this specific texture is used by the engine to control the intensity of environment map reflections. A brighter alpha value results in a more mirror-like surface.10  
  * TextureName-normal.dds: This is a **normal map**, used to add surface detail without increasing polygon count. The FS2O engine expects a specific format for these maps, often referred to as a DXT5\_NM format. The directional information is primarily stored in the Green and Alpha channels, a technical detail that must be handled correctly when processing these textures.10  
* **Animated Textures:** The engine supports animated textures on model surfaces, which can be implemented in two ways. The first is via the legacy .ANI format. The second, more modern method is to use an .EFF file. This is a simple text file that defines a sequence of static image files (e.g., RunningLights\_0000.dds, RunningLights\_0001.dds, etc.) and a frame rate, effectively creating an animation loop.10

### **1.4 The .ANI Animation Format**

The .ANI format is used throughout WCS for various 2D animated effects. It is a proprietary format specific to the *Freespace* engine.

* **Disambiguation:** It is imperative to distinguish the Freespace .ANI format from the common Microsoft Windows Animated Cursor file format, which also uses the .ani extension.23 The two formats are structurally unrelated, and attempting to use libraries designed for one to parse the other will fail. The Freespace format is a bespoke animation container.  
* **Technical Specification:** The format's structure has been documented by the modding community, providing a clear path for implementation.23  
  * **Header (ani\_header):** A fixed-size header contains essential metadata, including the file version, image dimensions (w, h), the total number of frames (nframes), and the playback speed in frames per second (fps).  
  * **Palette:** The header contains a 256-color RGB palette. This indicates the format's legacy origins in an era of indexed color graphics. The conversion process will need to use this palette to convert the indexed pixel data into full 24-bit or 32-bit color.  
  * **Image Data:** The image data for each frame is compressed using a run-length encoding (RLE) scheme similar to that of the .PCX format. A special packer\_code byte signifies that the next byte is a repeat count. A unique feature is its handling of transparency: a pixel value of 254 is treated as a transparent pixel. To render a frame with transparent pixels, the engine must have the pixel data from the *previous* frame, as the transparent areas reveal what was behind them in the preceding frame. This dependency between frames is a key aspect of the decoding logic.23  
* **Usage in WCS:** .ANI files are used for a variety of purposes within the game. These include weapon effects like explosions, animated interface elements such as the "talking heads" of characters during in-mission communication, and the animated graphics used in command briefings.8 The appropriate conversion strategy for an  
  .ANI file depends heavily on its context of use.

### **1.5 Tabular Data Integration (ships.tbl & weapons.tbl)**

The .tbl files are the brain of the FS2O engine's gameplay systems. They are simple, plain-text, key-value database files that are easily modified by modders to create new ships, weapons, and rebalance the game.12 They represent the "single source of truth" for the properties of game objects, and their data must be integrated with the visual assets for a functional conversion.

* **Role of .tbl files:** These files contain the vast majority of the game's numerical data. Any property that affects gameplay—from ship speed to laser damage to AI behavior—is defined in a .tbl file.5 The conversion process must parse these files to extract the data relevant to each 3D model.  
* **ships.tbl Structure:** This file contains a separate entry for every ship class in the game. Each entry is a collection of key-value pairs that define the ship's physical and gameplay properties. Key fields that must be extracted include 12:  
  * $Name: The unique string identifier for the ship class. This is the crucial key that links this data entry to a specific .pof file.  
  * $Mass: and $Moment of Inertia:: These floating-point values are fundamental to the ship's physics simulation, affecting its acceleration, turning rate, and response to collisions.11  
  * $Allowed PBanks and $Allowed SBanks: These are lists of weapon names (from weapons.tbl) that are permitted to be mounted on the ship's primary and secondary weapon hardpoints, respectively. This data is essential for implementing a weapon loadout system.12  
  * Numerous other fields define properties like shield and hull strength, maximum speed, afterburner characteristics, and AI behavior flags.  
* **weapons.tbl Structure:** In a similar fashion, this file defines the properties of every weapon in the game, from simple lasers to complex beam cannons and homing missiles. Key fields include 13:  
  * $Name: The unique string identifier for the weapon.  
  * $Damage:, $Velocity:, and $Lifetime:: The core performance statistics that determine the weapon's effectiveness. The effective range is typically calculated as $Velocity \* $Lifetime.  
  * $Armor Factor: and $Shield Factor:: Damage multipliers that define how effective the weapon is against hull plating versus energy shields.  
  * $Flags: A list of string-based flags that enable special behaviors. For example, the "EMP" flag makes the weapon an electromagnetic pulse weapon that disables electronics, while the "Esuck" flag allows it to drain energy from the target.

## **Section 2: C++ Converter Architecture and Code Review**

With a comprehensive understanding of the source asset formats established, the focus now shifts to the practical implementation of a conversion tool. A simple, monolithic script is insufficient for handling the complexity of the composite asset structure. A robust, maintainable, and extensible tool requires a well-defined architecture built on modern C++ principles and established software design patterns. This section provides a constructive critique of common implementation pitfalls and proposes a professional-grade software architecture for a new or refactored converter.

### **2.1 Critique of the Existing Implementation**

While the user's specific source code is not available for direct review, it is possible to anticipate common deficiencies based on the challenges inherent in parsing complex, legacy binary formats. A hypothetical review of a typical first-pass implementation would likely identify issues in the following areas.

* **Completeness:** The most significant and probable flaw is an incomplete understanding of the "composite asset." A converter focused solely on parsing the geometry from .pof files is fundamentally deficient. Such a tool would fail to:  
  * Integrate critical physics and gameplay data from ships.tbl and weapons.tbl. Without this, the converted models would be mere visual shells, lacking mass, weapon mounts, or any game-ready properties.  
  * Implement the file-system-aware discovery of associated texture maps. It would likely only load the base color map specified in the .pof and miss the crucial \-glow, \-shine, and \-normal maps, resulting in flat, lifeless materials.10  
  * Extract and preserve the rich set of metadata points (gun mounts, subsystems, dock points, etc.) that are essential for gameplay logic.11  
* **Binary Parsing Robustness:** Handling legacy binary data is fraught with peril. Common errors include:  
  * **Incorrect Data Type Sizing:** Using standard C++ types like int or short is not portable, as their size can vary between platforms. A robust parser must use fixed-size integer types from the \<cstdint\> header, such as uint32\_t and int16\_t, to ensure that the data is read correctly regardless of the compilation environment.  
  * **Ignoring Endianness:** The .pof format uses little-endian byte order. While this matches modern x86/x64 architectures, a truly portable tool should explicitly handle byte swapping for potential compilation on big-endian systems.  
  * **Mishandling of Chunk Length:** As noted in Section 1.2.2, a frequent mistake is to forget that the .pof chunk's length field excludes its own 8-byte header, leading to cascading file-pointer misalignment and corrupted data reads.9  
  * **Lack of Error Handling:** The code should gracefully handle file-not-found errors, corrupted chunks, and unexpected data values rather than crashing or producing undefined behavior. Using C++ iostreams in binary mode (std::ios::binary) or C-style fread for direct memory reads are standard approaches, but they must be paired with rigorous error checking.35  
* **Memory Management:** The hierarchical nature of .pof sub-objects and the traversal of BSP trees can lead to complex object graphs in memory. A C-style approach using manual new and delete is highly susceptible to memory leaks. Modern C++ practices, particularly the use of smart pointers (std::unique\_ptr for unique ownership, std::shared\_ptr for shared ownership), should be employed to automate memory management and ensure resource safety (RAII).  
* **Code Structure:** A common anti-pattern in simple conversion tools is tight coupling. The logic for parsing a .pof file is often intertwined directly with the code that writes the output format. This makes the tool inflexible and difficult to maintain. If a new output format were desired (e.g., FBX instead of glTF), or if a new input feature were discovered, large portions of the code would need to be rewritten. This monolithic design is a primary target for refactoring.

### **2.2 Recommended C++ Libraries and Dependencies**

Building a modern C++ application does not mean reinventing the wheel. Leveraging high-quality, well-maintained open-source libraries is essential for productivity and correctness. The following technology stack is recommended for building a professional-grade conversion tool.

| Task | Recommended Library | Key Features | Justification |  |
| :---- | :---- | :---- | :---- | :---- |
| **glTF 2.0 Serialization** | **tinygltf** 37 or | **fastgltf** 38 | Header-only, JSON parsing, binary buffer management, extension support. | tinygltf is the industry standard—stable, widely used, and reliable. fastgltf is a newer, performance-oriented alternative using modern C++17/20 and SIMD, making it an excellent choice if processing thousands of assets quickly is a priority. |
| **3D Mathematics** | **GLM (OpenGL Mathematics)** 40 | Header-only, GLSL-like syntax for vectors, matrices, quaternions. | GLM's syntax is immediately familiar to anyone with graphics programming experience. It is lightweight, robust, and designed specifically for the types of transformations (rotations, translations, projections) required in an asset pipeline. Alternatives like Eigen are powerful but may be overkill.41 |  |
| **DDS Texture I/O** | **DirectXTex (Microsoft)** 42 | Comprehensive support for all DDS variants, DXT compression/decompression, mipmap generation. | As the official Microsoft library for the DirectDraw Surface format, it is the most correct and complete solution for handling the .DDS files used by FS2O. It correctly handles the various DXT compression schemes and pixel formats. |  |
| **General Image I/O** | **stb\_image.h** | Single-header public domain library for loading PNG, TGA, PCX, and other formats. | stb\_image is a simple, effective, and ubiquitous solution for reading the non-DDS texture formats like .PCX and .TGA that may be encountered in legacy WCS assets. Its single-header nature makes it trivial to integrate into a project. |  |

This curated stack provides robust, pre-built solutions for the most complex parts of the conversion task—glTF writing, image decoding, and 3D math—allowing the developer to focus on the core logic of parsing the proprietary Freespace formats.

### **2.3 A Robust Software Architecture: Applying Design Patterns**

To address the structural weaknesses identified in the critique, a new architecture based on established software design patterns is proposed. This architecture decouples the major components of the application, leading to a system that is more flexible, maintainable, and easier to debug and extend.43 The core of the design is a three-stage pipeline:  
**Load \-\> Transform \-\> Save**.

#### **2.3.1 The Core Pipeline**

This model separates the concerns of reading source data, processing it, and writing destination data. Each stage operates independently, communicating through a set of well-defined, intermediate data structures. These structures are engine-agnostic, representing the "pure" data of the asset (e.g., struct IntermediateMesh { std::vector\<Vertex\> vertices;... };) without any ties to either the .pof or glTF format.

#### **2.3.2 Loader Stage (Input)**

This stage is responsible for parsing the various source files and populating the intermediate data structures. To manage the different file formats, the **Factory Method** pattern is ideal.43

* An abstract ILoader interface would define a common Load(filePath) method.  
* Concrete classes like PofLoader, TblLoader, and DdsLoader would implement this interface.  
* A central LoaderFactory would be responsible for creating the appropriate loader based on the file extension.

This design isolates the complex parsing logic for each file type into its own class. If support for a new file format is needed in the future, a new loader class can be added without modifying any existing parsing code.

#### **2.3.3 Transformer Stage (Logic)**

This stage acts as the bridge between the intermediate data structures populated by the loaders and the API of the glTF serialization library. The **Adapter** pattern is perfectly suited for this role.43

* An AssetAdapter class would take the IntermediateModel, IntermediateMaterial, and IntermediateShipStats objects as input.  
* It would expose methods that map this data to the concepts required by the glTF writer (e.g., GetGltfNodes(), GetGltfMeshes(), GetGltfMaterials()).

This adapter contains the core "business logic" of the conversion—for example, the heuristics for approximating PBR materials or the logic for creating glTF nodes from .pof metadata points. It cleanly separates the "what" (our intermediate data) from the "how" (the specific API calls needed to build a glTF file).

#### **2.3.4 Saver Stage (Output)**

This stage is responsible for constructing the final, complex glTF file. The glTF 2.0 format is a rich scene graph with meshes, materials, nodes, skins, and animations. Assembling this structure can be complex. The **Builder** pattern provides an elegant solution for this step-by-step construction process.43

* A GltfBuilder class would encapsulate the tinygltf or fastgltf library.  
* It would provide a high-level, fluent interface for constructing the asset, with methods like AddMesh(meshData), AddPbrMaterial(materialData), CreateNode(transform), and AddExtras(jsonData).  
* The AssetAdapter from the transformer stage would use this GltfBuilder to systematically construct the glTF scene.

This architecture transforms a potentially monolithic and confusing script into a clean, modular system. The PofLoader knows nothing about glTF, and the GltfBuilder knows nothing about .pof. They communicate only through the intermediate data structures and the adapter, making the entire system robust, testable, and extensible.

## **Section 3: The Definitive Conversion Pipeline: From .POF to glTF 2.0**

This section provides a practical, step-by-step blueprint for the conversion process, synthesizing the file format analysis from Section 1 with the software architecture proposed in Section 2\. It details the flow of data from the legacy WCS formats through the intermediate representation and into the final glTF 2.0 asset, ready for engine integration.

### **3.1 Stage 1: Parsing and Abstracting Legacy Data**

The initial stage of the pipeline is concerned with discovering all relevant files for a given asset and parsing them into the engine-agnostic intermediate data structures. This process must be holistic, treating the asset as the composite entity it is.

* **Asset Discovery and Pre-loading:** The conversion process should not begin with a single .pof file. Instead, it should be pointed at a directory containing the extracted contents of the WCS .vp archives. The first step is to invoke the TblLoader to parse ships.tbl and weapons.tbl. This builds a complete in-memory database or lookup table of all ship and weapon properties, indexed by their string names (e.g., "Hermes", "Subach HL-7"). This data must be available before any model processing begins.  
* **Loading the Composite Asset:** When the tool is instructed to convert a specific ship, for instance hermes.pof, it executes the following sequence:  
  1. The LoaderFactory creates a PofLoader instance, which is used to parse hermes.pof. The loader traverses the binary chunks, reconstructs the mesh geometry from the BSP tree, and extracts the sub-object hierarchy and all metadata points (guns, thrusters, etc.). This populates an IntermediateModel structure.  
  2. The loader extracts the list of texture names (e.g., "hermes\_a.dds") from the .pof's 'TXTR' chunk.  
  3. For each base texture name, the tool performs a file-system search for its variants. It looks for hermes\_a-glow.dds, hermes\_a-shine.dds, and hermes\_a-normal.dds.  
  4. The LoaderFactory creates a DdsLoader (or PcxLoader as needed) for each discovered texture file. The pixel data from these files is loaded and stored in an IntermediateMaterial structure, which is then associated with the relevant mesh parts in the IntermediateModel.  
  5. Finally, the tool uses the ship's name ("Hermes") as a key to query the pre-loaded table data. The corresponding entry from ships.tbl is retrieved and its contents are used to populate an IntermediateShipStats structure, which is then linked to the IntermediateModel.

At the end of this stage, the application holds a complete, in-memory representation of the Hermes scout drone, containing its geometry, all associated texture maps, and all of its gameplay-relevant physics and properties, entirely decoupled from the proprietary source formats.

### **3.2 Stage 2: Translating Geometry, Materials, and Animations**

This stage involves the core transformation logic, where the data from the intermediate structures is mapped to the concepts and structures of the glTF 2.0 specification.

#### **3.2.1 Geometry Conversion**

* **Node Hierarchy:** The sub-object hierarchy from the .pof file is translated directly into a glTF node hierarchy. The root node of the glTF scene will represent the ship itself, and child nodes will be created for each sub-object (turrets, debris, etc.), preserving their local transformations (position, rotation) relative to their parent.  
* **Mesh Data:** The vertex and index data reconstructed from the .pof's BSP tree for each sub-object is converted into glTF accessors and buffer views. This data becomes a glTF mesh primitive, which is then assigned to the corresponding node in the hierarchy.  
* **Levels of Detail (LODs):** Sub-objects identified as LODs can be handled in two ways. The simpler approach is to export each LOD as a separate mesh and node, allowing for manual setup in Godot. A more advanced approach would be to use the MSFT\_lod glTF extension, which allows for explicitly defining LOD levels and screen coverage distances within the glTF file itself, enabling automatic LOD switching in compatible renderers.

#### **3.2.2 Material Translation: The PBR Approximation Problem**

This is the most nuanced part of the conversion, as it requires mapping a legacy, non-photorealistic material system to the modern, physically-based PBR Metallic-Roughness model that is standard in glTF 2.0 and Godot.46 There is no perfect one-to-one mapping; the process relies on intelligent, configurable heuristics to achieve a visually pleasing and plausible result.

* A new glTF material will be created for each unique set of textures.  
* **Base Color:** The base color map (TextureName.dds) is straightforwardly assigned to the baseColorTexture slot in the PBR material.  
* **Emissive:** The glow map (TextureName-glow.dds) is assigned to the emissiveTexture slot. Since glow maps in FS2O are additive, an appropriate emissiveFactor (e.g., a value greater than 1.0 to create a bloom effect) should be set in the material. This factor can be exposed as a configurable parameter in the converter to allow for artistic tuning.  
* **Metallic & Roughness:** These properties do not exist in the source assets and must be derived from the specular (-shine) map. The following heuristic is proposed:  
  1. **Roughness Map:** The primary function of a roughness map is to control the blurriness of reflections. In the FS2O engine, the alpha channel of the \-shine map controls the intensity of environment map reflections.10 A sharp reflection corresponds to a smooth surface (low roughness), while a dull reflection corresponds to a rough surface (high roughness). Therefore, the alpha channel of the  
     \-shine map can be inverted and used as the green channel of a new texture, which will serve as the roughness map. (glTF standardly uses the G channel for roughness).  
  2. **Metallic Map:** The primary function of a metallic map is to distinguish between metal and non-metal (dielectric) surfaces. This is more difficult to derive. A possible heuristic is to use the luminance (brightness) of the RGB channels of the \-shine map. Areas with very bright, strong specular highlights are more likely to be metallic. A threshold can be applied: if the luminance is above a certain value (e.g., 0.9), the corresponding pixel in the metallic map (stored in the B channel of the same texture as roughness) is set to 1.0 (metal); otherwise, it is set to 0.0 (non-metal). These thresholds should be configurable.  
* **Normal Map:** The FS2O-specific normal map (TextureName-normal.dds) must be processed. If it stores data in the Green and Alpha channels, it needs to be converted to a standard tangent-space normal map (where X, Y, and Z directions are stored in the R, G, and B channels) before being assigned to the normalTexture slot in the glTF material.

#### **3.2.3 Animation Conversion**

* **Animated Textures:** For .ANI or .EFF files used as animated textures on a model, the best approach is to convert the sequence of frames into a single texture atlas or "sprite sheet." The animation metadata (frame count, dimensions of each frame, and fps) is then stored in the extras data of the glTF material that uses this texture. A custom shader in Godot can then be used to scroll the UV coordinates on the mesh to play the animation, driven by the metadata.  
* **Interface Animations:** For animations like "talking heads," which are not part of a 3D model, direct conversion to glTF is inappropriate. These should be converted into a more suitable format, such as a modern video format (Ogg Theora, which FS2O itself supports 28) or a sequence of PNG images with transparency, to be played back on a 2D UI plane in Godot.

### **3.3 Stage 3: Embedding Game-Specific Metadata**

A core principle of this conversion pipeline is the preservation of all gameplay-critical data. The glTF 2.0 specification provides a standard mechanism for this: the extras field, a JSON object where any custom, application-specific data can be stored.46 This feature is the key to creating fully functional, game-ready assets.  
The mapping from WCS features to their glTF representation is a critical design step that ensures no data is lost and that the resulting asset is easy to consume in Godot.

| WCS / FS2O Feature | glTF 2.0 Representation |
| :---- | :---- |
| POF Root Object | glTF Scene Root Node |
| POF Sub-Object (e.g., Hull, Turret) | glTF Child Node with associated glTF Mesh |
| POF Geometry (from BSP Tree) | glTF Mesh Primitive (Vertices, Indices, Normals, UVs) |
| POF Texture (TextureName.dds) | glTF Material pbrMetallicRoughness.baseColorTexture |
| POF Texture (-glow.dds) | glTF Material emissiveTexture |
| POF Texture (-shine.dds) | Heuristically converted to pbrMetallicRoughness.metallicRoughnessTexture |
| POF Texture (-normal.dds) | glTF Material normalTexture |
| POF Metadata Point (Gun, Missile, Dock) | Empty glTF Node at the correct transform (position/rotation) |
| POF Subsystem (Bounding Volume) | Empty glTF Node with a custom extras field defining the volume shape and size |
| ships.tbl Data (Mass, Inertia, etc.) | JSON object in the extras field of the glTF Scene Root Node |
| weapons.tbl Data (for hardpoints) | JSON object in the extras field of the corresponding glTF Gun/Missile Node |

The most effective way to embed the positional metadata is to represent it physically within the glTF scene graph. Instead of creating a simple list of coordinates, the converter will create empty glTF Node objects at the precise 3D position and orientation of each metadata point from the .pof file.

* The root node's extras field will contain the ship's global properties from ships.tbl: {"mass": 120.0, "moment\_of\_inertia": \[x, y, z\], "max\_speed": 150.0,...}.  
* An empty glTF node named gun\_mount\_0 will be created at the position and orientation of the first primary weapon hardpoint. Its extras field will contain its specific properties: {"type": "gun\_mount", "bank\_index": 0, "allowed\_weapons":}.  
* Another empty node named thruster\_point\_0 will be created at an engine nozzle location, with extras data like: {"type": "engine\_thruster", "radius": 2.5}.

This approach makes the asset "self-describing." When imported into Godot, these empty nodes become Node3D objects in the scene tree, correctly positioned and ready to be processed by a script. This turns a complex data-mapping problem into a much simpler scene composition task within the Godot editor.

## **Section 4: Seamless Integration with the Godot Engine**

The final stage of the pipeline is the consumption and setup of the generated glTF assets within the Godot Engine. A truly "seamless" integration goes beyond simply importing a model; it involves automating the process of configuring the imported scene into a fully functional, game-ready object. This is achieved by leveraging Godot's powerful glTF importer, its physics systems, and its editor scripting capabilities.

### **4.1 Leveraging Godot's Advanced glTF Importer**

Godot's support for the glTF 2.0 format is mature and robust, and it is the engine's officially recommended format for 3D assets.48 The engine's importer provides a wealth of options for controlling how assets are brought into a project.

* **Recommended Format:** While Godot can import text-based .gltf files, the binary .glb format is recommended for the final assets. A .glb file packages the JSON scene description, binary mesh data, and all textures into a single, self-contained file. This simplifies asset management and distribution significantly.50  
* **Import Settings:** The Godot editor's Import dock allows for fine-grained control over the import process. Settings for mesh compression, material handling, and animation import can be configured and saved on a per-asset basis. The converter should produce glTF files that are compatible with Godot's default settings, but users should be aware of these options for optimization and troubleshooting.

### **4.2 Automated Collision Shape Generation**

A renderable mesh is useless for gameplay without a corresponding physics collision shape. The pipeline must include a strategy for generating these shapes. Several methods are viable, ranging from manual to fully automated.

* **Strategy 1: In-Engine Manual Generation:** The simplest method is to perform this step manually within the Godot editor. After importing a model, a StaticBody3D or RigidBody3D node can be made the parent of the mesh. Then, by selecting the MeshInstance3D node, the user can access the "Mesh" menu at the top of the 3D viewport and select an option like "Create Trimesh Static Body" or "Create Single Convex Collision Sibling." This will automatically generate a CollisionShape3D node with a shape that matches the visual mesh.51 This is suitable for one-off conversions or prototyping but is not scalable for a large number of assets.  
* **Strategy 2: Import-Time Automated Generation:** Godot 4 features a significantly improved import system that can automate collision generation. In the Import dock, under the "Physics" section for the selected glTF file, the user can specify that a physics body should be generated. Options are available to create static, rigid, or character bodies, and to generate collision shapes using various methods (e.g., Trimesh, Convex Decomposition).54 This is a powerful, automated workflow. The old Godot 3 convention of using a  
  \-col suffix in a mesh name to trigger collision generation has been superseded by these more explicit import settings.54  
* **Strategy 3: Converter-Generated Collision Geometry:** This is the most robust and faithful approach. The original .pof file contains a BSP tree, which is itself a form of collision geometry. The C++ conversion tool can be enhanced to parse this BSP data and generate a simplified collision mesh. This collision mesh can be exported as a separate, non-rendered mesh within the same glTF file (e.g., named hermes\_colmesh). In Blender, a common convention is to create a simplified mesh and name it with a \-col or \-colonly suffix to mark it as collision geometry.56 The Godot importer can then be configured to use this specific mesh to generate the  
  CollisionShape3D, rather than using the high-poly visual mesh. This method provides the highest fidelity to the original game's physics representation and offers the best performance, as collision meshes can be significantly simpler than render meshes.

### **4.3 Post-Import Scripting and Asset Setup**

This final step is the key to achieving a truly seamless and automated pipeline. It bridges the gap between the imported, data-rich glTF file and a fully configured, game-ready Godot scene. This is accomplished by creating a Godot EditorImportPlugin or a tool script that executes automatically after the asset has been imported.50  
The existence of the custom metadata embedded in the extras field is what enables this automation. Without that data, this step would have to be done manually, which is slow, tedious, and error-prone. The post-import script is the consumer of the data that the C++ converter so carefully preserved and structured.  
The script's logic would be as follows:

1. **Access the Imported Scene:** The script gets a reference to the root node of the newly imported scene.  
2. **Apply Root Properties:** It accesses the extras JSON data on the root node. It reads keys like "mass" and "max\_speed" and applies these values to the corresponding properties of the root RigidBody3D node (e.g., root.mass \= extras\["mass"\]).  
3. **Traverse and Configure Child Nodes:** The script then recursively traverses the scene's node hierarchy.  
4. **Identify Metadata Nodes:** It looks for the special empty nodes that were created to represent metadata points (e.g., nodes named gun\_mount\_\*, thruster\_point\_\*, etc.).  
5. **Instance and Attach Sub-Scenes:** When it finds a metadata node, it reads its extras data to determine its purpose.  
   * If extras\["type"\] \== "engine\_thruster", the script will load a pre-made GPUParticles3D scene for an engine thruster effect, instance it, and add it as a child of the thruster node, ensuring it is correctly positioned and oriented.  
   * If extras\["type"\] \== "gun\_mount", the script might attach a generic weapon mount script to that node. This script, at runtime, would then use the allowed\_weapons data from the extras field to determine which weapon scenes can be equipped at that location.

This automated process transforms the static imported model into a dynamic, fully configured PackedScene. The final output of the entire conversion pipeline is therefore not just a collection of .glb files, but the .glb files *plus* the Godot tool script that understands how to interpret their embedded data. This completes the workflow, delivering assets that are not just ready to be dropped into a level, but are ready for immediate use in the game.

#### **Works cited**

1. Total conversions \- FreeSpace Wiki, accessed August 22, 2025, [https://wiki.hard-light.net/index.php/Total\_conversions](https://wiki.hard-light.net/index.php/Total_conversions)  
2. Wing Commander Saga, a fan-made interquel 11 years in the making, featuring 55 missions, 70 cinematics and 11.000 lines of dialogue, based on the Freespace 2 engine, finally has a release date: the 22nd of March. : r/Games \- Reddit, accessed August 22, 2025, [https://www.reddit.com/r/Games/comments/r2hzr/wing\_commander\_saga\_a\_fanmade\_interquel\_11\_years/](https://www.reddit.com/r/Games/comments/r2hzr/wing_commander_saga_a_fanmade_interquel_11_years/)  
3. Freespace 2 Mods \- Games \- Quarter To Three Forums, accessed August 22, 2025, [https://forum.quartertothree.com/t/freespace-2-mods/72505](https://forum.quartertothree.com/t/freespace-2-mods/72505)  
4. Wing Commander Saga Klavs Ship Pack, accessed August 22, 2025, [https://www.wcnews.com/chatzone/threads/wing-commander-saga-klavs-ship-pack.28782/](https://www.wcnews.com/chatzone/threads/wing-commander-saga-klavs-ship-pack.28782/)  
5. Where do I find ship statistics? \- Wing Commander Saga, accessed August 22, 2025, [https://wcsaga.com/index.php/forum-sp-468/2-vacuum-breather/6001-where-do-i-find-ship-statistics.html](https://wcsaga.com/index.php/forum-sp-468/2-vacuum-breather/6001-where-do-i-find-ship-statistics.html)  
6. How to edit a campaign mission in wing commander saga? \- Hard Light Productions, accessed August 22, 2025, [https://www.hard-light.net/forums/index.php?topic=92566.0](https://www.hard-light.net/forums/index.php?topic=92566.0)  
7. Downloads \- Wing Commander Saga, accessed August 22, 2025, [https://www.wcsaga.com/index.php/rs-downloads.html?folder=tools](https://www.wcsaga.com/index.php/rs-downloads.html?folder=tools)  
8. Tools \- The FreeSpace Oracle, accessed August 22, 2025, [http://www.fs2downloads.com/tools.html](http://www.fs2downloads.com/tools.html)  
9. POF data structure \- FreeSpace Wiki, accessed August 22, 2025, [https://wiki.hard-light.net/index.php/POF\_data\_structure](https://wiki.hard-light.net/index.php/POF_data_structure)  
10. Texturing \- FreeSpace Wiki, accessed August 22, 2025, [https://wiki.hard-light.net/index.php/Texturing](https://wiki.hard-light.net/index.php/Texturing)  
11. ModelView \- FreeSpace Wiki, accessed August 22, 2025, [https://wiki.hard-light.net/index.php/ModelView](https://wiki.hard-light.net/index.php/ModelView)  
12. How to make Shivan ships playable? :: Freespace 2 General Discussions, accessed August 22, 2025, [https://steamcommunity.com/app/273620/discussions/0/1697175413692479503/](https://steamcommunity.com/app/273620/discussions/0/1697175413692479503/)  
13. Weapons.tbl \- FreeSpace Wiki, accessed August 22, 2025, [https://wiki.hard-light.net/index.php/Weapons.tbl](https://wiki.hard-light.net/index.php/Weapons.tbl)  
14. 6.2.3.4. Creating the POF File \- Intel, accessed August 22, 2025, [https://www.intel.com/content/www/us/en/docs/programmable/683689/current/creating-the-pof-file.html](https://www.intel.com/content/www/us/en/docs/programmable/683689/current/creating-the-pof-file.html)  
15. 1.7.1.2.1. .pof Generation through Convert Programming Files \- Intel, accessed August 22, 2025, [https://www.intel.com/content/www/us/en/docs/programmable/683661/current/pof-generation-through-convert-programming.html](https://www.intel.com/content/www/us/en/docs/programmable/683661/current/pof-generation-through-convert-programming.html)  
16. Application Note 214 \- Arm, accessed August 22, 2025, [https://documentation-service.arm.com/static/5ed11bfdca06a95ce53f9000?token=](https://documentation-service.arm.com/static/5ed11bfdca06a95ce53f9000?token)  
17. POF File Extension: What Is It & How To Open It? \- Solvusoft, accessed August 22, 2025, [https://www.solvusoft.com/en/file-extensions/file-extension-pof/](https://www.solvusoft.com/en/file-extensions/file-extension-pof/)  
18. Extract Models from Freespace 2 \- Hard Light Productions, accessed August 22, 2025, [https://www.hard-light.net/forums/index.php?topic=87823.0](https://www.hard-light.net/forums/index.php?topic=87823.0)  
19. Details for 'POF Construction Suite 2' \- Wing Commander Saga, accessed August 22, 2025, [https://wcsaga.com/index.php/component/rsfiles/details.html?path=tools%2FPCS2\_2.0.3\_2008-05-15.exe\&Itemid=10001](https://wcsaga.com/index.php/component/rsfiles/details.html?path=tools/PCS2_2.0.3_2008-05-15.exe&Itemid=10001)  
20. Downloads \- FreeSpace Source Code Project, accessed August 22, 2025, [https://scp.indiegames.us/downloads.php?download=POFCS2](https://scp.indiegames.us/downloads.php?download=POFCS2)  
21. Why many games use .dds for texture files ? : r/gamedev \- Reddit, accessed August 22, 2025, [https://www.reddit.com/r/gamedev/comments/i1767n/why\_many\_games\_use\_dds\_for\_texture\_files/](https://www.reddit.com/r/gamedev/comments/i1767n/why_many_games_use_dds_for_texture_files/)  
22. fs2\_open \- manual page for FreeSpace 2 Open \- Ubuntu Manpage, accessed August 22, 2025, [https://manpages.ubuntu.com/manpages/noble/man6/fs2\_open\_3.7.4\_DEBUG.6.html](https://manpages.ubuntu.com/manpages/noble/man6/fs2_open_3.7.4_DEBUG.6.html)  
23. ANI formal definition \- FreeSpace Wiki, accessed August 22, 2025, [https://wiki.hard-light.net/index.php/ANI\_formal\_definition](https://wiki.hard-light.net/index.php/ANI_formal_definition)  
24. wiki.hard-light.net, accessed August 22, 2025, [https://wiki.hard-light.net/index.php/ANI\_formal\_definition\#:\~:text=Introduction,that%20make%20together%20the%20ANImation.](https://wiki.hard-light.net/index.php/ANI_formal_definition#:~:text=Introduction,that%20make%20together%20the%20ANImation.)  
25. ANI (file format) \- Wikipedia, accessed August 22, 2025, [https://en.wikipedia.org/wiki/ANI\_(file\_format)](https://en.wikipedia.org/wiki/ANI_\(file_format\))  
26. ANI File Format \- Daubnet, accessed August 22, 2025, [https://www.daubnet.com/en/file-format-ani](https://www.daubnet.com/en/file-format-ani)  
27. What is an ANI file and how can you open it? \- YouTube, accessed August 22, 2025, [https://www.youtube.com/watch?v=PP6ZLfUUJ9o](https://www.youtube.com/watch?v=PP6ZLfUUJ9o)  
28. Multimedia Files \- FreeSpace Wiki, accessed August 22, 2025, [https://wiki.hard-light.net/index.php/Multimedia\_Files](https://wiki.hard-light.net/index.php/Multimedia_Files)  
29. \[Demo Release\] Wing Commander Vega Assault \- Hard Light Productions, accessed August 22, 2025, [https://www.hard-light.net/forums/index.php?topic=98153.0](https://www.hard-light.net/forums/index.php?topic=98153.0)  
30. altering ship specs \- Wing Commander Saga, accessed August 22, 2025, [https://www.wcsaga.com/index.php/forum-sp-468/22-mods/7302-altering-ship-specs.html](https://www.wcsaga.com/index.php/forum-sp-468/22-mods/7302-altering-ship-specs.html)  
31. WC: Saga Source Code released \- Wing Commander CIC, accessed August 22, 2025, [https://www.wcnews.com/chatzone/threads/wc-saga-source-code-released.27158/](https://www.wcnews.com/chatzone/threads/wc-saga-source-code-released.27158/)  
32. Ship choice in simulator \- Wing Commander Saga, accessed August 22, 2025, [https://www.wcsaga.com/index.php/forum-sp-468/20-gameplay-a-strategy-discussion/6793-ship-choice-in-simulator.html](https://www.wcsaga.com/index.php/forum-sp-468/20-gameplay-a-strategy-discussion/6793-ship-choice-in-simulator.html)  
33. Game settings.tbl \- FreeSpace Wiki, accessed August 22, 2025, [https://wiki.hard-light.net/index.php/Game\_settings.tbl](https://wiki.hard-light.net/index.php/Game_settings.tbl)  
34. Ships.tbl \- FreeSpace Wiki, accessed August 22, 2025, [https://wiki.hard-light.net/index.php/Ships.tbl](https://wiki.hard-light.net/index.php/Ships.tbl)  
35. Binary Files in C++, accessed August 22, 2025, [http://www.eecs.umich.edu/courses/eecs380/HANDOUTS/cppBinaryFileIO-2.html](http://www.eecs.umich.edu/courses/eecs380/HANDOUTS/cppBinaryFileIO-2.html)  
36. C++ cstdio fread() \- Read Binary Data \- Vultr Docs, accessed August 22, 2025, [https://docs.vultr.com/cpp/standard-library/cstdio/fread](https://docs.vultr.com/cpp/standard-library/cstdio/fread)  
37. syoyo/tinygltf: Header only C++11 tiny glTF 2.0 library \- GitHub, accessed August 22, 2025, [https://github.com/syoyo/tinygltf](https://github.com/syoyo/tinygltf)  
38. Overview — fastgltf 0.7.2 documentation, accessed August 22, 2025, [https://fastgltf.readthedocs.io/v0.7.x/overview.html](https://fastgltf.readthedocs.io/v0.7.x/overview.html)  
39. spnda/fastgltf: A modern C++17 glTF 2.0 library focused on speed, correctness, and usability, accessed August 22, 2025, [https://github.com/spnda/fastgltf](https://github.com/spnda/fastgltf)  
40. C++ Math libraries | LibHunt, accessed August 22, 2025, [https://cpp.libhunt.com/libs/math](https://cpp.libhunt.com/libs/math)  
41. Eigen C++ \- TuxFamily.org, accessed August 22, 2025, [https://eigen.tuxfamily.org/index.php?title=Main\_Page](https://eigen.tuxfamily.org/index.php?title=Main_Page)  
42. Programming Guide for DDS \- Win32 apps | Microsoft Learn, accessed August 22, 2025, [https://learn.microsoft.com/en-us/windows/win32/direct3ddds/dx-graphics-dds-pguide](https://learn.microsoft.com/en-us/windows/win32/direct3ddds/dx-graphics-dds-pguide)  
43. Design Patterns in C++ \- Refactoring.Guru, accessed August 22, 2025, [https://refactoring.guru/design-patterns/cpp](https://refactoring.guru/design-patterns/cpp)  
44. Basic Design Patterns in C++ \- Medium, accessed August 22, 2025, [https://medium.com/must-know-computer-science/basic-design-patterns-in-c-39bd3d477a5c](https://medium.com/must-know-computer-science/basic-design-patterns-in-c-39bd3d477a5c)  
45. Adapter Pattern | C++ Design Patterns \- GeeksforGeeks, accessed August 22, 2025, [https://www.geeksforgeeks.org/system-design/adapter-pattern-c-design-patterns/](https://www.geeksforgeeks.org/system-design/adapter-pattern-c-design-patterns/)  
46. Introducing the Godot glTF 2.0 scene exporter – Godot Engine, accessed August 22, 2025, [https://godotengine.org/article/introducing-the-godot-gltf-2-0-scene-exporter/](https://godotengine.org/article/introducing-the-godot-gltf-2-0-scene-exporter/)  
47. Blender animation distorted in Godot 4.2 \- Reddit, accessed August 22, 2025, [https://www.reddit.com/r/godot/comments/195tgvp/blender\_animation\_distorted\_in\_godot\_42/](https://www.reddit.com/r/godot/comments/195tgvp/blender_animation_distorted_in_godot_42/)  
48. Importing assets \- Godot Forums, accessed August 22, 2025, [https://godotforums.org/d/39422-importing-assets](https://godotforums.org/d/39422-importing-assets)  
49. What 3d model format is best for godot \- Reddit, accessed August 22, 2025, [https://www.reddit.com/r/godot/comments/1in7t7s/what\_3d\_model\_format\_is\_best\_for\_godot/](https://www.reddit.com/r/godot/comments/1in7t7s/what_3d_model_format_is_best_for_godot/)  
50. Available 3D formats — Godot Engine (4.4) documentation in English, accessed August 22, 2025, [https://docs.godotengine.org/en/4.4/tutorials/assets\_pipeline/importing\_3d\_scenes/available\_formats.html](https://docs.godotengine.org/en/4.4/tutorials/assets_pipeline/importing_3d_scenes/available_formats.html)  
51. Importing 3D Objects :: Godot 4 Recipes \- KidsCanCode.org, accessed August 22, 2025, [https://kidscancode.org/godot\_recipes/4.x/g101/3d/101\_3d\_02/index.html](https://kidscancode.org/godot_recipes/4.x/g101/3d/101_3d_02/index.html)  
52. What 3D file format do you use? : r/godot \- Reddit, accessed August 22, 2025, [https://www.reddit.com/r/godot/comments/ugqud1/what\_3d\_file\_format\_do\_you\_use/](https://www.reddit.com/r/godot/comments/ugqud1/what_3d_file_format_do_you_use/)  
53. Collision shapes (3D) — Godot Engine (latest) documentation in ..., accessed August 22, 2025, [https://docs.godotengine.org/en/latest/tutorials/physics/collision\_shapes\_3d.html](https://docs.godotengine.org/en/latest/tutorials/physics/collision_shapes_3d.html)  
54. Level design just got way easier : r/godot \- Reddit, accessed August 22, 2025, [https://www.reddit.com/r/godot/comments/1fwxcmt/level\_design\_just\_got\_way\_easier/](https://www.reddit.com/r/godot/comments/1fwxcmt/level_design_just_got_way_easier/)  
55. New 3D import: GLTF importer creates no collision for \-col objects · Issue \#48945 · godotengine/godot \- GitHub, accessed August 22, 2025, [https://github.com/godotengine/godot/issues/48945](https://github.com/godotengine/godot/issues/48945)  
56. How To Export Collision Shapes Out of Blender Into Godot\! Godot Quick Tip\! \- YouTube, accessed August 22, 2025, [https://www.youtube.com/shorts/rC3h1vumRxQ](https://www.youtube.com/shorts/rC3h1vumRxQ)  
57. Blender 4 add on for creating custom collision meshes and GDScript to import them, accessed August 22, 2025, [https://forum.godotengine.org/t/blender-4-add-on-for-creating-custom-collision-meshes-and-gdscript-to-import-them/68883](https://forum.godotengine.org/t/blender-4-add-on-for-creating-custom-collision-meshes-and-gdscript-to-import-them/68883)  
58. Exporting 3D scenes — Godot Engine (4.4) documentation in English, accessed August 22, 2025, [https://docs.godotengine.org/en/4.4/tutorials/assets\_pipeline/exporting\_3d\_scenes.html](https://docs.godotengine.org/en/4.4/tutorials/assets_pipeline/exporting_3d_scenes.html)