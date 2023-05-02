#![warn(clippy::all)]

use std::{
    io::{self, Read},
    iter::zip,
    thread::sleep,
    time::{Duration, Instant},
};

fn check_password(buffer: &str) -> io::Result<bool> {
    let start_time = Instant::now();

    let real_password = String::from_utf8(xor(&PASSWORD_ENCRYPTED, &XOR_BYTES)).unwrap();

    if real_password.chars().count() == buffer.chars().count() {
        let mut iter = zip(buffer.chars(), real_password.chars()).peekable();

        while let Some((input, password)) = iter.next() {
            if input.is_ascii() {
                if input != password {
                    break;
                }
                if iter.peek().is_none() {
                    return Ok(true);
                }
            } else {
                println!("Only ASCII characters are expected!");
                break;
            }
        }
    } else {
        println!("Wrong length");
    }
    sleep(Duration::new(0, 100_000_000) - Instant::now().duration_since(start_time));
    println!("Wrong password, try again");
    Ok(false)
}

fn handle_client() -> io::Result<()> {
    loop {
        let mut buffer = [0; 2048];
        // I don't use the .lines() iterator because I don't want some sneaky baker sending unlimited length strings, now we limit it to 2048 bytes and discard if no endline is included.
        let mut stdin = io::stdin();
        let n = stdin.read(&mut buffer[..])?;

        if n == 0 {
            return Ok(());
        }

        let buffered_string = String::from_utf8_lossy(&buffer).into_owned();
        let attempt = buffered_string.split_once('\n');

        if let Some((buffer, _)) = attempt {
            #[cfg(debug_assertions)]
            dbg!(&buffer);
            if check_password(buffer)? {
                    println!("Successfully unlocked! password was: {}", buffer);
                return Ok(());
            }
        }
    }
}

fn xor<'a>(source: &'a [u8], key: &'a [u8]) -> Vec<u8> {
    if key.is_empty() {
        source.to_vec()
    } else {
        let mut result = Vec::new();
        let mut it = key.iter().cycle();
        for i in source {
            result.push(i ^ it.next().unwrap());
        }
        result
    }
}

const PASSWORD_LENGTH: usize = 72;
const XOR_BYTES: [u8; PASSWORD_LENGTH] = [
	196, 172, 107, 226, 184, 180, 27, 62, 135, 83, 168, 110, 54, 171, 155, 145, 126, 158, 137, 231, 184, 52, 74, 150, 219, 143, 35, 96, 182, 98, 30, 93, 62, 197, 88, 210, 24, 33, 104, 92, 31, 30, 78, 120, 51, 225, 131, 157, 161, 246, 179, 212, 114, 213, 178, 72, 123, 160, 14, 185, 227, 67, 66, 136, 230, 193, 225, 52, 88, 175, 8, 174
];
const PASSWORD_ENCRYPTED: [u8; PASSWORD_LENGTH] = [
	177, 194, 15, 151, 204, 207, 77, 75, 206, 20, 210, 42, 70, 227, 213, 227, 31, 201, 234, 128, 219, 7, 30, 210, 171, 200, 18, 21, 215, 53, 43, 51, 114, 172, 26, 131, 122, 108, 39, 110, 123, 86, 0, 11, 82, 182, 231, 173, 232, 190, 253, 228, 43, 141, 248, 120, 34, 248, 71, 222, 185, 20, 118, 239, 191, 178, 174, 88, 60, 232, 57, 211
];

fn main() -> io::Result<()> {
    #[cfg(debug_assertions)]
    assert_eq!(
        &PASSWORD_ENCRYPTED,
        xor(b"undut{VuIGzDpHNraWcgc3TDpG1uaW5nLiBQbMO2dHNsaWd0IHN0YXJ0YXIgZW4gYsOldG1}", &XOR_BYTES).as_slice()
    );
	println!("Welcome to the challenge! The task is to find the password for this system, one expects a newline ('\\n') at the end of a password attempt.");
    println!("Enter your password:");
    match handle_client()
    {
    	Ok(_) => {},
        Err(_err) => {
            #[cfg(debug_assertions)]
            println!("Connect attempted failed: {_err}");
        }
    }
    Ok(())
}
