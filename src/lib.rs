use std::sync::{Arc, Mutex};
use pyo3::{wrap_pyfunction, prelude::*};
use rayon::prelude::*;
use std::collections::HashMap;
use std::thread;
use pyo3::types::PyDict;

#[pyfunction]
fn counter<'a>(inp: &'a str) -> HashMap<&'a str, usize> {
    let mut rizz: HashMap<&str, usize> = HashMap::new();
    for item in inp.split_ascii_whitespace() {
        *rizz.entry(item).or_insert(0) += 1;
    }
    rizz
}

#[pyfunction]
fn par_counter<'a>(inp: &'a str) -> HashMap<&'a str, usize> {
    inp
        .split_ascii_whitespace()
        .collect::<Vec<_>>()
        .par_iter()
        .fold(HashMap::new, |mut acc, &item| {
            *acc.entry(item).or_insert(0) += 1;
            acc
        })
        .reduce(HashMap::new, |mut acc, item| {
            for (key, value) in item {
                *acc.entry(key).or_insert(0) += value;
            }
            acc
        })
}

fn words_counter(text: String) -> HashMap<String, usize> {
    let mut word_counts = HashMap::new();
    for word in text.split_whitespace() {
        *word_counts.entry(word.to_owned()).or_insert(0) += 1;
    }
    word_counts
}

#[pyfunction]
fn thread_counter(text: String) -> PyResult<Py<PyAny>> {
    let num_threads = 12;
    let text_len = text.len();
    let chunk_size = text_len / num_threads;

    let word_count = Arc::new(Mutex::new(HashMap::new()));
    let mut handles = vec![];

    for i in 0..num_threads {
        let start = i * chunk_size;
        let mut end = if i == num_threads - 1 {
            text_len
        } else {
            (i + 1) * chunk_size
        };

        // Prevent cutting a word in half
        if let Some(pos) = text[start..end].rfind(|c: char| c.is_whitespace()) {
            end = start + pos;
        }

        // Clone the chunk to give each thread ownership
        let chunk = text[start..end].to_string(); // <-- Fixed here
        let word_count = Arc::clone(&word_count);

        let handle = thread::spawn(move || {
            let counts = words_counter(chunk);
            let mut word_count = word_count.lock().unwrap();
            for (word, count) in counts {
                *word_count.entry(word).or_insert(0) += count;
            }
        });

        handles.push(handle);
    }

    for handle in handles {
        handle.join().unwrap();
    }

    let word_count = Arc::try_unwrap(word_count).unwrap().into_inner().unwrap();

    Python::with_gil(|py| {
        let py_dict = PyDict::new(py);
        for (word, count) in word_count {
            py_dict.set_item(word, count)?;
        }
        Ok(py_dict.into())
    })
}


#[pymodule]
fn plib(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(counter, m)?)?;
    m.add_function(wrap_pyfunction!(par_counter, m)?)?;
    m.add_function(wrap_pyfunction!(thread_counter, m)?)?;
    Ok(())
}
