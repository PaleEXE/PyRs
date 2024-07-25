use pyo3::{wrap_pyfunction, prelude::*};
use rayon::prelude::*;
use std::collections::HashMap;

#[pyfunction]
fn counter<'a>(inp: &'a str) -> HashMap<&'a str, usize>{
    let mut rizz: HashMap<&str, usize> = HashMap::new();
    for item in inp.split(" "){
        *rizz.entry(item).or_insert(0) += 1;
    }
    rizz
}
#[pyfunction]
fn show(txt: String){
    println!("{txt}");
    if txt == "Majd"{println!("Did you mean Moon?")}
}
#[pyfunction]
fn par_counter<'a>(inp: &'a str) -> HashMap<&'a str, usize>{
    inp
        .split_ascii_whitespace()
        .collect::<Vec<_>>()
        .par_iter()
        .fold(HashMap::new, |mut acc, item| {
            *acc.entry(*item).or_insert(0) += 1;
            acc
        })
        .reduce(HashMap::new, |mut acc, item| {
            for (key, value) in item {
                *acc.entry(key).or_insert(0) += value;
            }
            acc
        })
}

#[pymodule]
fn plib(m: &Bound<'_, PyModule>) -> PyResult<()>{
    m.add_function(wrap_pyfunction!(counter, m)?)?;
    m.add_function(wrap_pyfunction!(par_counter, m)?)?;
    m.add_function(wrap_pyfunction!(show, m)?)?;
    Ok(())
}
