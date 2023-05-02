string flag = File.ReadAllText("/home/ctf/flag.txt");

Guid guid = Guid.NewGuid();
string file = Path.Join(Path.GetTempPath(), guid.ToString());

bool isAdmin = false;

Console.WriteLine("Hej och välkommen till min server.");
while (true)
{
    Console.WriteLine($"Du har GUID:et {guid.ToString()}. Vad vill du göra?");
    Console.WriteLine("1. Logga in som annat GUID");
    Console.WriteLine("2. Bli flaggläsare");
    if (!isAdmin)
        Console.WriteLine("3. Få flagga");
    Console.WriteLine("4. Avsluta");

    if (!int.TryParse(Console.ReadLine(), out int menuOption))
    {
        Console.WriteLine("Ange ett giltigt menyval.");
        break;
    }

    Console.Clear();
    switch (menuOption)
    {
        case 1:
            Console.WriteLine("Vilket GUID vill du identifiera dig som?");
            if (!Guid.TryParse(Console.ReadLine(), out Guid g))
            {
                Console.WriteLine("Ange ett giltigt GUID.");
                File.Delete(file);
                return;
            }
            File.Delete(file);
            file = Path.Join(Path.GetTempPath(), g.ToString());
            guid = g;
	    break;

        case 2:
            if (isAdmin)
            {
                Console.WriteLine("Du är redan flaggläsare.");
                break;
            }
            File.WriteAllText(file, "1");
            isAdmin = true;
            Console.WriteLine("Du är numera flaggläsare.");
            break;

        case 3:
            if (isAdmin)
		Console.WriteLine("Ange ett giltigt menyval.");
            else if (File.Exists(file) && File.ReadAllText(file) == "1")
            {
		Console.WriteLine("Varsågod. Flaggan är " + flag);
                break;
            }
            else
                Console.WriteLine("Du är inte flaggläsare.");
            break;

        case 4:
            File.Delete(file);
            return;
    }
}
