# Hello World, no packaging.

## Create a java file

```
$ ed Main.java
a
class Main {
    public static void main(String[] args) {
        System.out.println("Hello World!"); // Display the string.
    }
}
.
w
q
```

## Compile it

```
$ javac Main.java
$ java -cp . Main

```

