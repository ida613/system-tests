package com.datadoghq.system_tests.springboot;

import com.datadoghq.system_tests.iast.utils.*;
import io.opentracing.Span;
import io.opentracing.util.GlobalTracer;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import javax.naming.Context;
import javax.naming.NamingException;
import javax.naming.directory.InitialDirContext;
import javax.servlet.ServletException;
import javax.servlet.ServletRequest;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.sql.DataSource;
import java.io.IOException;
import java.util.Hashtable;

@RestController
@RequestMapping("/iast")
public class AppSecIast {
    String superSecretAccessKey = "insecure";

    private final SqlExamples sqlExamples;
    private final CmdExamples cmdExamples;
    private final PathExamples pathExamples;
    private final CryptoExamples cryptoExamples;
    private volatile LDAPExamples ldapExamples;
    private final SsrfExamples ssrfExamples;
    private final WeakRandomnessExamples weakRandomnessExamples;


    public AppSecIast(final DataSource dataSource) {
        this.sqlExamples = new SqlExamples(dataSource);
        this.cmdExamples = new CmdExamples();
        this.pathExamples = new PathExamples();
        this.cryptoExamples = new CryptoExamples();
        this.ssrfExamples = new SsrfExamples();
        this.weakRandomnessExamples = new WeakRandomnessExamples();
    }

    @RequestMapping("/insecure_hashing/deduplicate")
    String removeDuplicates() {
        return cryptoExamples.removeDuplicates(superSecretAccessKey);
    }

    @RequestMapping("/insecure_hashing/multiple_hash")
    String multipleInsecureHash() {
        return cryptoExamples.multipleInsecureHash(superSecretAccessKey);
    }

    @RequestMapping("/insecure_hashing/test_secure_algorithm")
    String secureHashing() {
        final Span span = GlobalTracer.get().activeSpan();
        if (span != null) {
            span.setTag("appsec.event", true);
        }
        return cryptoExamples.secureHashing(superSecretAccessKey);
    }

    @RequestMapping("/insecure_hashing/test_md5_algorithm")
    String insecureMd5Hashing() {
        final Span span = GlobalTracer.get().activeSpan();
        if (span != null) {
            span.setTag("appsec.event", true);
        }
        return cryptoExamples.insecureMd5Hashing(superSecretAccessKey);
    }

    @RequestMapping("/insecure_cipher/test_secure_algorithm")
    String secureCipher() {
        final Span span = GlobalTracer.get().activeSpan();
        if (span != null) {
            span.setTag("appsec.event", true);
        }
        return cryptoExamples.secureCipher(superSecretAccessKey);
    }

    @RequestMapping("/insecure_cipher/test_insecure_algorithm")
    String insecureCipher() {
        final Span span = GlobalTracer.get().activeSpan();
        if (span != null) {
            span.setTag("appsec.event", true);
        }
        return cryptoExamples.insecureCipher(superSecretAccessKey);
    }

    @PostMapping("/unvalidated_redirect/test_secure_header")
    public String secureHeader(HttpServletResponse response) {
        response.setHeader("location", "http://dummy.location.com");
        return "redirect";
    }

    @PostMapping("/unvalidated_redirect/test_insecure_header")
    public String insecureHeader(final ServletRequest request, final HttpServletResponse response) {
        final String location = request.getParameter("location");
        response.setHeader("location", location);
        return "redirect";
    }

    @PostMapping("/unvalidated_redirect/test_secure_redirect")
    public String secureRedirect(HttpServletResponse response) throws IOException {
        response.sendRedirect("http://dummy.location.com");
        return "redirect";
    }

    @PostMapping("/unvalidated_redirect/test_insecure_redirect")
    public String insecureRedirect(final ServletRequest request, final HttpServletResponse response) throws IOException {
        final String location = request.getParameter("location");
        response.sendRedirect(location);
        return "redirect";
    }

    @PostMapping("/unvalidated_redirect/test_secure_forward")
    public String secureForward(HttpServletRequest request, final HttpServletResponse response) throws ServletException, IOException {
        request.getRequestDispatcher("http://dummy.location.com").forward(request, response);
        return "redirect";
    }

    @PostMapping("/unvalidated_redirect/test_insecure_forward")
    public String insecureForward(final ServletRequest request, final HttpServletResponse response) throws IOException, ServletException {
        final String location = request.getParameter("location");
        request.getRequestDispatcher(location).forward(request, response);
        return "redirect";
    }

    @PostMapping("/sqli/test_insecure")
    Object insecureSql(final ServletRequest request) {
        final Span span = GlobalTracer.get().activeSpan();
        if (span != null) {
            span.setTag("appsec.event", true);
        }
        final String username = request.getParameter("username");
        final String password = request.getParameter("password");
        return sqlExamples.insecureSql(username, password);
    }

    @PostMapping("/sqli/test_secure")
    Object secureSql(final ServletRequest request) {
        final Span span = GlobalTracer.get().activeSpan();
        if (span != null) {
            span.setTag("appsec.event", true);
        }
        final String username = request.getParameter("username");
        final String password = request.getParameter("password");
        return sqlExamples.secureSql(username, password);
    }

    @PostMapping("/cmdi/test_insecure")
    String insecureCmd(final ServletRequest request) {
        final Span span = GlobalTracer.get().activeSpan();
        if (span != null) {
            span.setTag("appsec.event", true);
        }
        final String cmd = request.getParameter("cmd");
        return cmdExamples.insecureCmd(cmd);
    }

    @PostMapping("/ldapi/test_insecure")
    String insecureLDAP(final ServletRequest request) {
        final Span span = GlobalTracer.get().activeSpan();
        if (span != null) {
            span.setTag("appsec.event", true);
        }
        final String username = request.getParameter("username");
        final String password = request.getParameter("password");
        return getOrCreateLdapExamples().injection(username, password);
    }

    @PostMapping("/ldapi/test_secure")
    String secureLDAP() {
        final Span span = GlobalTracer.get().activeSpan();
        if (span != null) {
            span.setTag("appsec.event", true);
        }
        return getOrCreateLdapExamples().secure();
    }


    @PostMapping("/path_traversal/test_insecure")
    String insecurePathTraversal(final ServletRequest request) {
        final Span span = GlobalTracer.get().activeSpan();
        if (span != null) {
            span.setTag("appsec.event", true);
        }
        final String path = request.getParameter("path");
        return pathExamples.insecurePathTraversal(path);
    }

    @PostMapping("/ssrf/test_insecure")
    String insecureSsrf(final ServletRequest request) {
        final String url = request.getParameter("url");
        return ssrfExamples.insecureUrl(url);
    }

    @GetMapping("/weak_randomness/test_insecure")
    String insecureRandom() {
        return weakRandomnessExamples.weakRandom();
    }

    @GetMapping("/weak_randomness/test_secure")
    String secureRandom() {
        return weakRandomnessExamples.secureRandom();
    }

    /**
     * TODO: Ldap is failing to startup in native image this method ensures it's started lazily
     *
     * Native reflection configuration for com.sun.jndi.ldap.LdapCtxFactory is missing.
     */
    private LDAPExamples getOrCreateLdapExamples() {
        if (ldapExamples == null) {
            try {
                Hashtable<String, String> env = new Hashtable<>(3);
                env.put(Context.INITIAL_CONTEXT_FACTORY, "com.sun.jndi.ldap.LdapCtxFactory");
                env.put(Context.PROVIDER_URL, "ldap://localhost:8389/dc=example");
                env.put(Context.SECURITY_AUTHENTICATION, "none");
                this.ldapExamples = new LDAPExamples(new InitialDirContext(env));
            } catch (NamingException e) {
                throw new RuntimeException(e);
            }
        }
        return ldapExamples;
    }
}
