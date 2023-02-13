import java.io.BufferedInputStream;
import java.io.InputStream;

class RunCmd {

    public static void main(String[] args) {

        System.out.println("Get current runtime");
        Runtime currentRuntime = Runtime.getRuntime();

        if (args.length <= 0) {
            System.err.println("No runnable commands!");
            System.exit(1);
        }

        StringBuilder cmdBuilder = new StringBuilder();

        for (String cmd : args) {
            cmdBuilder.append(cmd).append(" ");
        }

        final String runCmd = cmdBuilder.toString();
        System.out.printf("Cmd: '%s'\n", runCmd);

        try {
            Process process = currentRuntime.exec(runCmd);
            int waitCode = process.waitFor();
            if (0 != waitCode) {
                System.out.printf("WaitFor() -> code: %s \n", waitCode);
            }

            int exitCode = process.exitValue();
            if (0 != exitCode) {
                InputStream errStream = process.getErrorStream();
                BufferedInputStream errBufferStream = new BufferedInputStream(errStream);
                int readResult = errBufferStream.read();

                System.out.printf("Exit code '%s', err message '%s'", exitCode, readResult);
                System.exit(exitCode);
            }

            InputStream inputStream = process.getInputStream();

            BufferedInputStream inputStreamBuf = new BufferedInputStream(inputStream);

            byte[] buf = new byte[1024];

            StringBuilder cmdResulet = new StringBuilder();
            while (-1 != inputStreamBuf.read(buf)) {
                cmdBuilder.append(cmdBuilder);
            }

            System.out.println(cmdResulet.toString());

        } catch (Exception e) {
            System.err.printf(e.getMessage());
        }
    }
}