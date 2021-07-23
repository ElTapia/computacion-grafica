// CAMBIAR DIRECCION CAMARA A 1.0, 0.0, -1.0

use std::fs::File;

use rpt::*;

fn main() -> color_eyre::Result<()> {
    color_eyre::install()?;

    let mut scene = Scene::new();

    // Agregamos una mesa
    scene.add(
        Object::new(
            load_obj(File::open("examples/table.obj")?)?
                .scale(&glm::vec3(0.015, 0.015, 0.015))
                .rotate_y(glm::quarter_pi())
                .translate(&glm::vec3(0.0, -1.0, -0.3)),
        )
        .material(Material::metallic(hex_color(0xa18262), 0.4)),
    );

    // Agregamos mas sillas y mesas al lado de la mesa
    scene.add(
        Object::new(load_obj(File::open("examples/Table_And_Chairs.obj")?)?
            .scale(&glm::vec3(0.03, 0.03, 0.03))
            .translate(&glm::vec3(10.0, -1.0, 0.0))
        )
        .material(Material::metallic(hex_color(0xa18262), 0.4)),
    );

    // Agregamos un plano que simule un piso
    scene.add(
        Object::new(plane(glm::vec3(0.0, 1.0, 0.0), -1.0))
            .material(Material::diffuse(hex_color(0x787878))),
    );

    // Plano que simula el techo, para el eje Z
    scene.add(
        Object::new(plane(glm::vec3(0.0, 0.0, 1.0), -1.0)
            .translate(&glm::vec3(0.0, 0.0, -21.0))
        )
            .material(Material::diffuse(hex_color(0x4d4d4d))),
    );

    // Plano de techo para el eje X
    scene.add(
        Object::new(plane(glm::vec3(1.0, 0.0, 0.0), -1.0)
            .translate(&glm::vec3(21.0, 0.0, 0.0))
        )
            .material(Material::diffuse(hex_color(0x4d4d4d))),
    );

    // Agregamos una luz ambiental
    scene.add(Light::Ambient(glm::vec3(0.2, 0.2, 0.2)));

    // Agregamos un punto de luz
    scene.add(Light::Point(
        glm::vec3(1.0, 10.0, 1.0),
        glm::vec3(0.0, 2.0, 0.0),
    ));

    // Agregamos otro punto de luz
    scene.add(Light::Point(
        glm::vec3(10.0, 1.0, 1.0),
        glm::vec3(4.0, 2.0, 0.0),
    ));

    // Agregamos otro punto de luz
    scene.add(Light::Point(
        glm::vec3(1.0, 1.0, 10.0),
        glm::vec3(-4.0, 2.0, 0.0),
    ));

    // Agregamos otro punto de luz
    scene.add(Light::Point(
        glm::vec3(10.0, 1.0, 1.0),
        glm::vec3(10.0, 2.0, 0.0),
    ));

    // Agregamos otro punto de luz
    scene.add(Light::Point(
        glm::vec3(1.0, 1.0, 10.0),
        glm::vec3(30.0, 2.0, 0.0),
    ));

    // Seteamos la camara y creamos la imagen, para cambiar la camara, podemos modificar el archivo camera, así es más sencillo :D
    Renderer::new(&scene, Camera::default())
        .width(800)
        .height(800)
        .render()
        .save("back.png")?;

    Ok(())
}
